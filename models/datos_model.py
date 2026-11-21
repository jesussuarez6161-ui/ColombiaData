import json
import os

import pyodbc
from dotenv import load_dotenv

load_dotenv()


CAMPOS = {
    "id_api": ["cod_mpio", "codigo_municipio", "id", "codigo"],
    "municipio": ["nom_mpio", "municipio", "nombre_municipio"],
    "categoria": ["dpto", "departamento", "categoria"],
    "valor": ["tipo_municipio", "tipo", "valor"],
    "fecha_registro": ["fecha", "fecha_registro"],
}


def obtener_conexion():
    servidor = os.getenv("DB_SERVER")
    base_datos = os.getenv("DB_NAME")
    driver = os.getenv("DB_DRIVER", "ODBC Driver 18 for SQL Server")
    trusted = os.getenv("DB_TRUSTED", "yes").lower() == "yes"

    if trusted:
        cadena = (
            f"DRIVER={{{driver}}};"
            f"SERVER={servidor};"
            f"DATABASE={base_datos};"
            "Trusted_Connection=yes;"
            "TrustServerCertificate=yes;"
        )
    else:
        usuario = os.getenv("DB_USER")
        clave = os.getenv("DB_PASSWORD")
        cadena = (
            f"DRIVER={{{driver}}};"
            f"SERVER={servidor};"
            f"DATABASE={base_datos};"
            f"UID={usuario};PWD={clave};"
            "TrustServerCertificate=yes;"
        )

    return pyodbc.connect(cadena)


def _campo(registro, columna):
    for nombre in CAMPOS[columna]:
        valor = registro.get(nombre)
        if valor not in (None, ""):
            return str(valor)
    return None



def guardar_registros(registros):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    nuevos = 0
    omitidos = 0

    try:
        for registro in registros:
            identificador = _campo(registro, "id_api")

            if not identificador:
                omitidos += 1
                continue

            cursor.execute(
                "SELECT COUNT(*) FROM RegistrosAPI WHERE id_api = ?",
                identificador
            )

            existe = cursor.fetchone()[0]

            if existe > 0:
                omitidos += 1
                continue

            # Guardar solamente registros nuevos
            cursor.execute(
                """
                INSERT INTO RegistrosAPI
                    (id_api, municipio, categoria, valor,
                     fecha_registro, json_original)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                identificador,
                _campo(registro, "municipio"),
                _campo(registro, "categoria"),
                _campo(registro, "valor"),
                _campo(registro, "fecha_registro"),
                json.dumps(registro, ensure_ascii=False)
            )

            nuevos += 1

        conexion.commit()
        return nuevos, omitidos

    except Exception:
        conexion.rollback()
        raise

    finally:
        cursor.close()
        conexion.close()


def consultar_registros(filtro=""):
    """Devuelve hasta 100 registros; el filtro busca en municipio/categoría."""
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    try:
        if filtro:
            cursor.execute(
                """
                SELECT TOP 100 id_api, municipio, categoria,
                       valor, fecha_registro
                FROM RegistrosAPI
                WHERE municipio LIKE ?
                   OR categoria LIKE ?
                ORDER BY id DESC
                """,
                f"%{filtro}%",
                f"%{filtro}%",
            )
        else:
            cursor.execute(
                """
                SELECT TOP 100 id_api, municipio, categoria,
                       valor, fecha_registro
                FROM RegistrosAPI
                ORDER BY id DESC
                """
            )

        columnas = [columna[0] for columna in cursor.description]
        return [dict(zip(columnas, fila)) for fila in cursor.fetchall()]
    finally:
        cursor.close()
        conexion.close()


def obtener_resumen():
    """Resumen numérico básico: totales y top 5 de categorías."""
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    try:
        cursor.execute(
            """
            SELECT COUNT(*),
                   COUNT(DISTINCT municipio),
                   COUNT(DISTINCT categoria)
            FROM RegistrosAPI
            """
        )
        total, municipios, categorias = cursor.fetchone()

        cursor.execute(
            """
            SELECT TOP 5 categoria, COUNT(*) AS cantidad
            FROM RegistrosAPI
            WHERE categoria IS NOT NULL
            GROUP BY categoria
            ORDER BY cantidad DESC, categoria
            """
        )
        top = [{"categoria": fila[0], "cantidad": fila[1]} for fila in cursor.fetchall()]

        return {
            "total": total,
            "municipios": municipios,
            "categorias": categorias,
            "top_categorias": top,
        }
    finally:
        cursor.close()
        conexion.close()
