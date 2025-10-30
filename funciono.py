import requests
from bs4 import BeautifulSoup
import json
import os
import re

BASE_URL = "https://bogota.gov.co"
TAG_URL = f"{BASE_URL}/tag/cortes-de-agua-en-bogota"
DATA_PATH = "data/enlaces.json"

def obtener_enlaces():
    response = requests.get(TAG_URL)
    soup = BeautifulSoup(response.text, 'html.parser')
    enlaces = []

    # Expresión regular para detectar URLs relacionadas con cortes de agua
    patron = re.compile(r'/mi-ciudad/habitat/cortes-de-agua-en-bogota.*')

    for a in soup.find_all('a', href=True):
        href = a['href']
        if patron.match(href):
            enlaces.append(BASE_URL + href)

    return list(set(enlaces))

def guardar_enlaces(enlaces):
    os.makedirs("data", exist_ok=True)
    with open(DATA_PATH, "w", encoding="utf-8") as f:
        json.dump(enlaces, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    enlaces = obtener_enlaces()
    guardar_enlaces(enlaces)
    print(f"✅ Se guardaron {len(enlaces)} enlaces en {DATA_PATH}")