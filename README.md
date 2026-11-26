# API de novedades de inventario

API REST construida con **FastAPI** y **SQLite** para registrar y consultar solicitudes de novedades de inventario (diferencias, productos averiados, etc.).

## Requisitos

- Python 3.10 o superior

## Instalación

```bash
python -m venv .venv
.venv\Scripts\activate        # Windows
pip install -r requirements.txt
```

## Ejecución

```bash
python -m uvicorn app.main:app --reload
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
  "tienda": "Tienda Velez",
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

## Supuestos

| Campo | Regla |
|---|---|
| `id` | Obligatorio, entero positivo y único; lo envía el cliente |
| `tienda` | Obligatorio, 1 a 100 caracteres |
| `tipo` | `Diferencia de inventario`, `Producto averiado` u `Otro` |
| `descripcion` | Obligatorio, 1 a 500 caracteres |
| `prioridad` | `Alta`, `Media` o `Baja` |
| `estado` | `Pendiente` (por defecto), `En proceso` o `Resuelto` |
| `fecha_creacion` | La asigna el servidor en UTC |

- Los valores admitidos distinguen mayúsculas y minúsculas.
- Los espacios al inicio y al final se eliminan.
- No se aceptan campos desconocidos.

## Persistencia

Se eligió **SQLite** porque viene incluida en Python, no requiere servidor y conserva los datos al reiniciar. El `id` es llave primaria, por lo que la base de datos impide los duplicados.

## Pruebas

```powershell
python -m pytest test -v
```

Cada prueba usa una base de datos temporal.

| Caso | Resultado esperado | Resultado observado |
|---|---|---|
| Crear una solicitud válida | 201, estado `Pendiente` y `fecha_creacion` | PASSED |
| Repetir un `id` (error) | 409 y una sola solicitud guardada | PASSED |
| Prioridad `Urgente` (error) | 422 indicando el campo `prioridad` | PASSED |
| Omitir `tienda` (error) | 422 indicando el campo `tienda` | PASSED |
| Filtrar por `Pendiente` y `Alta` | 200 solo con la coincidencia | PASSED |

Ejecución en Windows con Python 3.12.4 y pytest 9.2.0: **5 passed, 1 warning**. La advertencia indica que el uso de `httpx` en el cliente de pruebas de Starlette está obsoleto y sugiere `httpx2`; no afectó los resultados.

## Estructura

```
app/
  main.py       # Endpoints y manejo de errores
  schemas.py    # Modelos y validaciones (Pydantic)
  database.py   # Acceso a SQLite
docs/           # Documentación adicional
test/           # Pruebas
```

## Decisión técnica descartada

**PostgreSQL:** exige instalar y configurar un servidor, un esfuerzo innecesario para este prototipo. Lo consideraría con varias instancias de la API o alta concurrencia.

## Limitación para una siguiente versión

No se puede cambiar el estado de una solicitud ya creada. El siguiente paso sería `PATCH /solicitudes/{id}` para completar el seguimiento. Tampoco hay autenticación ni paginación.

## Dependencias

`fastapi`, `uvicorn`, `pytest` y `httpx` (ver `requirements.txt`).

## Documentos

- [Mi experiencia](docs/experiencia.md)
- [Evolución de la solución](docs/evolucion.md)
- [Bitácora de IA](docs/bitacora_ia.md)

## Registro de trabajo

El avance está en el historial de commits.

**Tiempo real invertido:** 135 minutos.
