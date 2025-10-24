"""
app.py
------
API REST básica para exponer los cortes de luz almacenados.
"""

from flask import Flask, jsonify
import pandas as pd #type: ignore
from loguru import logger

app = Flask(__name__)

@app.route("/api/cortes", methods=["GET"])
def get_cortes():
    """Devuelve los datos de cortes en formato JSON."""
    try:
        df = pd.read_csv("data/cortes_bogota_detailed.csv")
        return jsonify(df.to_dict(orient="records"))
    except Exception as e:
        logger.error(f"Error leyendo datos: {e}")
        return jsonify({"error": "No se pudieron cargar los datos"}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5000)
