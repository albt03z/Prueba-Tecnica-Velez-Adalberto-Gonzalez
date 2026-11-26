from datetime import datetime
from enum import Enum

from pydantic import BaseModel, ConfigDict, Field


class Prioridad(str, Enum):
    ALTA = "Alta"
    MEDIA = "Media"
    BAJA = "Baja"


class Estado(str, Enum):
    PENDIENTE = "Pendiente"
    EN_PROCESO = "En proceso"
    RESUELTO = "Resuelto"


class Tipo(str, Enum):
    DIFERENCIA = "Diferencia de inventario"
    AVERIADO = "Producto averiado"
    OTRO = "Otro"


class SolicitudCrear(BaseModel):
    """Datos que envía el cliente."""

    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    id: int = Field(gt=0, le=2_147_483_647)
    tienda: str = Field(min_length=1, max_length=100)
    tipo: Tipo
    descripcion: str = Field(min_length=1, max_length=500)
    prioridad: Prioridad
    estado: Estado = Estado.PENDIENTE


class Solicitud(SolicitudCrear):
    """Solicitud guardada: la fecha la asigna el servidor."""

    fecha_creacion: datetime
