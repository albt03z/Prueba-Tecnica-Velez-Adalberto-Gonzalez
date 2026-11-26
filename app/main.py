import sqlite3
from contextlib import asynccontextmanager
from datetime import datetime, timezone

from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app import database
from app.schemas import Estado, Prioridad, Solicitud, SolicitudCrear

MENSAJES = {
    "missing": "Este campo es obligatorio",
    "extra_forbidden": "Campo no permitido",
    "string_too_short": "No puede estar vacío",
    "string_too_long": "Supera la longitud máxima",
    "string_type": "Debe ser un texto",
    "int_type": "Debe ser un número entero",
    "int_parsing": "Debe ser un número entero",
    "greater_than": "Debe ser mayor que 0",
    "less_than_equal": "El número es demasiado grande",
    "json_invalid": "El JSON está mal formado",
}


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Crea la tabla de SQLite al iniciar la aplicación."""
    database.crear_tabla()
    yield


app = FastAPI(title="API de novedades de inventario", lifespan=lifespan)


@app.exception_handler(RequestValidationError)
async def errores_de_validacion(request: Request, exc: RequestValidationError):
    """Convierte los errores de validación de Pydantic en mensajes en español (422)."""
    errores = []
    for error in exc.errors():
        tipo = error["type"]
        if tipo == "enum":
            permitidos = error["ctx"]["expected"].replace(" or ", " o ")
            mensaje = f"Valor no admitido. Use: {permitidos}"
        else:
            mensaje = MENSAJES.get(tipo, error["msg"])

        if tipo == "json_invalid":
            campo = "body"
        else:
            campo = str(error["loc"][-1])
        errores.append({"campo": campo, "mensaje": mensaje})

    return JSONResponse(
        status_code=422,
        content={"detail": "Datos inválidos", "errores": errores},
    )


@app.get("/health")
def health():
    """Verifica que el servicio está activo."""
    return {"status": "ok"}


@app.post("/solicitudes", response_model=Solicitud, status_code=201)
def crear_solicitud(datos: SolicitudCrear):
    """Registra una solicitud nueva (201). Responde 409 si el id ya existe."""
    solicitud = Solicitud(
        **datos.model_dump(),
        fecha_creacion=datetime.now(timezone.utc),
    )
    try:
        database.insertar(solicitud.model_dump(mode="json"))
    except sqlite3.IntegrityError:
        raise HTTPException(
            status_code=409,
            detail=f"Ya existe una solicitud con el id {datos.id}",
        )
    return solicitud


@app.get("/solicitudes", response_model=list[Solicitud])
def consultar_solicitudes(
    estado: Estado | None = None,
    prioridad: Prioridad | None = None,
):
    """Lista las solicitudes, con filtros opcionales por estado y prioridad."""
    return database.listar(
        estado=estado.value if estado else None,
        prioridad=prioridad.value if prioridad else None,
    )
