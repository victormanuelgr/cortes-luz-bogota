import sqlite3
import json
import os

DETALLES_PATH = "data/detalles.json"
DB_PATH = "data/cortes_agua.db"

def db_save():
    if not os.path.exists(DETALLES_PATH):
        print("❌ No se encontró el archivo de detalles.")
        return

    with open(DETALLES_PATH, "r", encoding="utf-8") as f:
        datos = json.load(f)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Crear tabla
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS cortes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url TEXT,
            localidad TEXT,
            corte TEXT
        )
    """)

    # Insertar cada corte como fila individual
    for item in datos:
        url = item.get("url", "")
        localidad = item.get("localidad", "")
        for corte in item.get("cortes", []):
            cursor.execute("INSERT INTO cortes (url, localidad, corte) VALUES (?, ?, ?)", (url, localidad, corte))

    conn.commit()
    conn.close()
    print(f"✅ Base de datos guardada en {DB_PATH}")

if __name__ == "__main__":
    db_save()