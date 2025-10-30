import requests #type: ignore
from bs4 import BeautifulSoup  # type: ignore
import re
import json
import os

SITEMAP_URL = "https://bogota.gov.co/sitemap.xml"
DATA_PATH = "data/enlaces.json"

def obtener_subsitemaps():
    """Obtiene todos los sub-sitemaps desde el sitemap principal."""
    response = requests.get(SITEMAP_URL)
    soup = BeautifulSoup(response.content, 'xml')
    return [loc.text.strip() for loc in soup.find_all('loc') if 'sitemap' in loc.text]

def obtener_enlaces_relevantes(subsitemaps):
    """Busca enlaces que contengan frases específicas sobre cortes de agua en Bogotá."""
    patron = re.compile(
        r'.*(cortes-de-agua-en-bogota|suspension-del-servicio-de-agua-en-bogota|barrios-sin-agua-en-bogota).*',
        re.IGNORECASE
    )
    enlaces = []

    for sitemap_url in subsitemaps:
        try:
            res = requests.get(sitemap_url)
            soup = BeautifulSoup(res.content, 'xml')
            for loc in soup.find_all('loc'):
                url = loc.text.strip()
                if patron.search(url):
                    enlaces.append(url)
        except Exception as e:
            print(f"⚠️ Error al procesar {sitemap_url}: {e}")

    return list(set(enlaces))

def guardar_enlaces(enlaces):
    """Guarda los enlaces en un archivo JSON."""
    os.makedirs("data", exist_ok=True)
    with open(DATA_PATH, "w", encoding="utf-8") as f:
        json.dump(enlaces, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    subsitemaps = obtener_subsitemaps()
    enlaces = obtener_enlaces_relevantes(subsitemaps)
    guardar_enlaces(enlaces)
    print(f"✅ Se guardaron {len(enlaces)} enlaces en {DATA_PATH}")