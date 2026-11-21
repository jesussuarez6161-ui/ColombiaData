import os

from dotenv import load_dotenv
from flask import Flask, flash, redirect, render_template, request, url_for

from api.api_client import APIClient
from models.datos_model import (
    consultar_registros,
    guardar_registros,
    obtener_resumen,
)

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "clave-local-solo-desarrollo")


@app.route("/", methods=["GET"])
def inicio():

    filtro = request.args.get("q", "").strip()
    try:
        registros = consultar_registros(filtro)
        resumen = obtener_resumen()
    except Exception as error:  # base de datos caída, tabla inexistente, etc.
        registros, resumen = [], None
        flash(f"No fue posible consultar la base de datos: {error}", "error")
    return render_template(
        "index.html",
        registros=registros,
        filtro=filtro,
        resumen=resumen,
    )


@app.route("/sincronizar", methods=["POST"])
def sincronizar():
    """Consulta la API, guarda los registros nuevos y vuelve al inicio."""
    try:
        cliente = APIClient()
        datos = cliente.obtener_registros(1200)
        nuevos, omitidos = guardar_registros(datos)
        flash(
            f"Consulta terminada. Recibidos: {len(datos)}. "
            f"Nuevos guardados: {nuevos}. Omitidos (ya existían o sin id): {omitidos}.",
            "success",
        )
    except Exception as error:
        flash(f"No fue posible consultar o guardar los datos: {error}", "error")
    return redirect(url_for("inicio"))


if __name__ == "__main__":
    # debug=True solo en el computador del estudiante (desarrollo local).
    app.run(debug=True)
