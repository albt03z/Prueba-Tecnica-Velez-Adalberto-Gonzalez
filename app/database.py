import os
import sqlite3
from contextlib import closing

DB_PATH = os.getenv("DB_PATH", "inventario.db")


def conectar() -> sqlite3.Connection:
    """Abre una conexión a SQLite cuyas filas se pueden leer por nombre de columna."""
    conexion = sqlite3.connect(DB_PATH)
    conexion.row_factory = sqlite3.Row
    return conexion


def crear_tabla() -> None:
    """Crea la tabla solicitudes si todavía no existe."""
    with closing(conectar()) as conexion, conexion:
        conexion.execute(
            """
            CREATE TABLE IF NOT EXISTS solicitudes (
                id             INTEGER PRIMARY KEY,
                tienda         TEXT NOT NULL,
                tipo           TEXT NOT NULL,
                descripcion    TEXT NOT NULL,
                prioridad      TEXT NOT NULL,
                estado         TEXT NOT NULL,
                fecha_creacion TEXT NOT NULL
            )
            """
        )


def insertar(solicitud: dict) -> None:
    """Lanza sqlite3.IntegrityError si el id ya existe."""
    with closing(conectar()) as conexion, conexion:
        conexion.execute(
            """
            INSERT INTO solicitudes
                (id, tienda, tipo, descripcion, prioridad, estado, fecha_creacion)
            VALUES
                (:id, :tienda, :tipo, :descripcion, :prioridad, :estado, :fecha_creacion)
            """,
            solicitud,
        )


def listar(estado: str | None = None, prioridad: str | None = None) -> list[dict]:
    """Devuelve las solicitudes (filtradas si se indica) ordenadas por fecha e id."""
    consulta = "SELECT * FROM solicitudes WHERE 1 = 1"
    parametros: list[str] = []

    if estado:
        consulta += " AND estado = ?"
        parametros.append(estado)
    if prioridad:
        consulta += " AND prioridad = ?"
        parametros.append(prioridad)

    consulta += " ORDER BY fecha_creacion, id"

    with closing(conectar()) as conexion:
        return [dict(fila) for fila in conexion.execute(consulta, parametros)]
