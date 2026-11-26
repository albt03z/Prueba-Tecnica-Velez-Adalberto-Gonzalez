# API de novedades de inventario

API REST construida con **FastAPI** y **SQLite** para registrar y consultar solicitudes de novedades de inventario (diferencias, productos averiados, etc.).

## Requisitos

- Python 3.10 o superior

## Instalación

```bash
python -m venv .venv
.venv\Scripts\activate        # Windows
# source .venv/bin/activate   # Linux / macOS
pip install -r requirements.txt
```

## Ejecución

```bash
uvicorn app.main:app --reload
```

La API queda en `http://127.0.0.1:8000`. La documentación interactiva (Swagger) está en `http://127.0.0.1:8000/docs`.

La base de datos se guarda en `inventario.db` y se crea sola al iniciar. Para cambiar la ruta, define la variable de entorno `DB_PATH`.

## Endpoints

| Método | Ruta           | Descripción                                      |
|--------|----------------|--------------------------------------------------|
| GET    | `/health`      | Verifica que el servicio está activo             |
| POST   | `/solicitudes` | Crea una solicitud (201). 409 si el `id` existe  |
| GET    | `/solicitudes` | Lista solicitudes. Filtros: `estado`, `prioridad`|

### Crear solicitud

`POST /solicitudes`

```json
{
  "id": 1,
  "tienda": "Tienda Centro",
  "tipo": "Producto averiado",
  "descripcion": "Caja dañada",
  "prioridad": "Alta"
}
```

| Campo         | Reglas                                                              |
|---------------|---------------------------------------------------------------------|
| `id`          | Entero entre 1 y 2.147.483.647, único                               |
| `tienda`      | Texto, 1 a 100 caracteres                                           |
| `tipo`        | `Diferencia de inventario`, `Producto averiado` u `Otro`            |
| `descripcion` | Texto, 1 a 500 caracteres                                           |
| `prioridad`   | `Alta`, `Media` o `Baja`                                            |
| `estado`      | Opcional: `Pendiente` (por defecto), `En proceso` o `Resuelto`      |

La respuesta incluye además `fecha_creacion`, asignada por el servidor. No se aceptan campos adicionales.

### Consultar solicitudes

```
GET /solicitudes?estado=Pendiente&prioridad=Alta
```

Ambos filtros son opcionales. Los resultados vienen ordenados por fecha de creación e id.

### Errores de validación

Los datos inválidos devuelven `422` con mensajes en español:

```json
{
  "detail": "Datos inválidos",
  "errores": [{ "campo": "prioridad", "mensaje": "Valor no admitido. Use: 'Alta', 'Media' o 'Baja'" }]
}
```

## Pruebas

```bash
pytest
```

## Estructura

```
app/
  main.py       # Endpoints y manejo de errores
  schemas.py    # Modelos y validaciones (Pydantic)
  database.py   # Acceso a SQLite
docs/           # Documentación adicional
test/           # Pruebas
```
