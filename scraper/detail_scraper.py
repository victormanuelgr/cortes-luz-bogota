import os
import json
import re
import requests #type: ignore
from bs4 import BeautifulSoup

ENLACES_PATH = "data/enlaces.json"
DETALLES_PATH = "data/detalles.json"

def cargar_enlaces():
    with open(ENLACES_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def extraer_detalles(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    texto = soup.get_text(separator="\n", strip=True)

    # Buscar bloques por localidad
    bloques = re.findall(r"Localidad de (.+?)(?=Localidad de|Recomendaciones|Consulta aquí|$)", texto, re.DOTALL)

    resultados = []
    for bloque in bloques:
        localidad_match = re.match(r"([A-Za-zÁÉÍÓÚÑñ ]+)", bloque)
        localidad = localidad_match.group(1).strip() if localidad_match else "Desconocida"

        cortes = re.findall(r"([^.]*?De la .*?hasta por \d+ horas.*?)\.", bloque)
        cortes_limpios = [c.strip() for c in cortes if "De la" in c or "Desde las" in c]

        if cortes_limpios:
            resultados.append({
                "url": url,
                "localidad": localidad,
                "cortes": cortes_limpios
            })

    return resultados

def guardar_detalles(todos):
    os.makedirs("data", exist_ok=True)
    with open(DETALLES_PATH, "w", encoding="utf-8") as f:
        json.dump(todos, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    enlaces = cargar_enlaces()
    todos_los_detalles = []

    for enlace in enlaces:
        print(f"🔍 Procesando: {enlace}")
        detalles = extraer_detalles(enlace)
        todos_los_detalles.extend(detalles)

    guardar_detalles(todos_los_detalles)
    print(f"✅ Se guardaron {len(todos_los_detalles)} registros en {DETALLES_PATH}")