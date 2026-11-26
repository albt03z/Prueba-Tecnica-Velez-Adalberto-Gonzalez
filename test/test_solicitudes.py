import pytest
from fastapi.testclient import TestClient
from app import database
from app.main import app

SOLICITUD = {
    "id": 1,
    "tienda": "Velez",
    "tipo": "Diferencia de inventario",
    "descripcion": "Faltan 3 unidades del producto Buzo de cuero L",
    "prioridad": "Alta",
    "estado": "Pendiente"
}

@pytest.fixture
def cliente(tmp_path, monkeypatch):
    """Crea un cliente de prueba para la API."""

    monkeypatch.setattr(database, "DB_PATH", str(tmp_path / "test.db"))
    with TestClient(app) as cliente:
        yield cliente

def test_crear_solicitud(cliente):
    """Crear una solicitud devuelve 201, conserva el estado y asigna fecha_creacion."""
    respuesta = cliente.post("/solicitudes", json=SOLICITUD)

    assert respuesta.status_code == 201
    assert respuesta.json()["estado"] == "Pendiente"
    assert "fecha_creacion" in respuesta.json()


def test_rechaza_id_duplicado(cliente):
    """Un id repetido devuelve 409 y no se guarda una segunda solicitud."""
    cliente.post("/solicitudes", json=SOLICITUD)
    respuesta = cliente.post("/solicitudes", json=SOLICITUD)

    assert respuesta.status_code == 409
    assert len(cliente.get("/solicitudes").json()) == 1


def test_rechaza_prioridad_invalida(cliente):
    """Una prioridad fuera del catálogo devuelve 422 señalando el campo prioridad."""
    respuesta = cliente.post(
        "/solicitudes", json={**SOLICITUD, "prioridad": "Urgente"}
    )

    assert respuesta.status_code == 422
    assert respuesta.json()["errores"][0]["campo"] == "prioridad"


def test_rechaza_campo_faltante(cliente):
    """Omitir un campo obligatorio devuelve 422 señalando el campo tienda."""
    datos = {k: v for k, v in SOLICITUD.items() if k != "tienda"}
    respuesta = cliente.post("/solicitudes", json=datos)

    assert respuesta.status_code == 422
    assert respuesta.json()["errores"][0]["campo"] == "tienda"


def test_filtra_por_estado_y_prioridad(cliente):
    """El listado filtra por estado y prioridad y devuelve solo las coincidencias."""
    cliente.post("/solicitudes", json=SOLICITUD)
    cliente.post("/solicitudes", json={**SOLICITUD, "id": 102, "prioridad": "Baja"})
    cliente.post(
        "/solicitudes", json={**SOLICITUD, "id": 103, "estado": "Resuelto"}
    )

    respuesta = cliente.get(
        "/solicitudes", params={"estado": "Pendiente", "prioridad": "Alta"}
    )

    assert respuesta.status_code == 200
    assert [s["id"] for s in respuesta.json()] == [1]