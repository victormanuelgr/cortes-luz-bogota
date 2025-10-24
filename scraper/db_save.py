"""
db_save.py
----------
Opcional: Guarda los resultados del scraping en una base de datos.
"""

import pandas as pd #type: ignore
import sqlite3
from loguru import logger

def save_to_sqlite(csv_path="data/cortes_bogota_detailed.csv", db_path="data/cortes.db"):
    """Guarda los datos del CSV en una base de datos SQLite local."""
    conn = sqlite3.connect(db_path)
    df = pd.read_csv(csv_path)
    df.to_sql("cortes_bogota", conn, if_exists="replace", index=False)
    conn.close()
    logger.success(f"Datos guardados en {db_path}")

if __name__ == "__main__":
    save_to_sqlite()
