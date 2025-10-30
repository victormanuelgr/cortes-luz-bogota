import pandas as pd
import sqlite3
import os

# Ruta al archivo .db
db_path = os.path.join('data', 'cortes_agua.db')

# Conexión a la base de datos
conn = sqlite3.connect(db_path)

# Mostrar las tablas disponibles
tables = pd.read_sql_query("SELECT name FROM sqlite_master WHERE type='table';", conn)
print("Tablas encontradas en la base de datos:")
print(tables)

# Elegir una tabla (ajusta el nombre si es diferente)
nombre_tabla = 'cortes'  # Cambia esto si tu tabla tiene otro nombre

# Leer los datos
df = pd.read_sql_query(f"SELECT * FROM {nombre_tabla};", conn)

# Exportar a Excel
excel_path = os.path.join('data', 'cortes_agua.xlsx')
df.to_excel(excel_path, index=False)

print(f"Datos exportados exitosamente a: {excel_path}")