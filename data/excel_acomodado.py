import pandas as pd
import os

ruta_excel = os.path.join(os.path.dirname(__file__), "cortes_agua.xlsx")
df = pd.read_excel(ruta_excel)

# Extraer todas las fechas
df['Fecha'] = df['url'].str.extract(r'(\d{1,2}-de-[a-zA-Z]+-\d{4})', expand=False)

# Convertir fechas a formato dd-mm-yyyy
meses = {
    'enero':'01', 'febrero':'02', 'marzo':'03', 'abril':'04',
    'mayo':'05', 'junio':'06', 'julio':'07', 'agosto':'08',
    'septiembre':'09', 'octubre':'10', 'noviembre':'11', 'diciembre':'12'
}

def convertir_fecha(texto):
    if pd.isna(texto):
        return ""
    for mes, num in meses.items():
        if mes in texto.lower():
            return texto.lower().replace(f"-de-{mes}-", f"-{num}-")
    return texto

df['Fecha'] = df['Fecha'].apply(convertir_fecha)

# 🔹 Rellenar fechas vacías con la fecha anterior
df['Fecha'] = df['Fecha'].replace("", pd.NA).fillna(method='ffill')

# Separar Dirección y Horario desde 'corte'
def separar_direccion_horario(texto):
    partes = texto.split("Desde", 1)
    direccion = partes[0].strip()
    horario = "Desde" + partes[1].strip() if len(partes) > 1 else ""
    return pd.Series([direccion, horario])

df[['Direccion', 'Horario']] = df['corte'].apply(separar_direccion_horario)

# Mantener solo columnas finales
df_final = df[['id', 'Fecha', 'localidad', 'Direccion', 'Horario']]

# Guardar Excel acomodado
ruta_guardado = os.path.join(os.path.dirname(__file__), "cortes_agua_acomodado.xlsx")
df_final.to_excel(ruta_guardado, index=False)

print(f"Excel acomodado creado en: {ruta_guardado}")
