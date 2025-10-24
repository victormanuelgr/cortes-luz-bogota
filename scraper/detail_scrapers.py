"""
detail_scraper.py
-----------------
Lee el listado generado por list_scraper.py, accede a cada artículo
y extrae los datos relevantes (localidad, barrios, horarios, etc.).
"""

import pandas as pd # type: ignore
from bs4 import BeautifulSoup
from loguru import logger
from .utils import get, random_sleep

def parse_detail(url):
    """
    Procesa una página de detalle de corte de luz.

    Args:
        url (str): enlace del artículo.

    Returns:
        dict: Información relevante del artículo.
    """
    logger.info(f"Extrayendo detalle: {url}")
    resp = get(url)
    soup = BeautifulSoup(resp.text, "html.parser")

    # Contenedor principal del texto
    content = soup.select_one("div.field--name-body")
    if not content:
        return {"url": url, "text": None, "barrios_info": []}

    text = content.get_text(separator="\n", strip=True)

    # Filtrar solo párrafos con información relevante
    barrios_info = []
    for p in content.find_all("p"):
        txt = p.get_text(strip=True)
        if any(k in txt.lower() for k in ["localidad", "barrio", "desde", "hasta", "horario"]):
            barrios_info.append(txt)

    return {"url": url, "text": text, "barrios_info": barrios_info}

def run(list_csv_path="data/cortes_bogota_listado.csv"):
    """
    Recorre el listado de artículos y extrae la información detallada.
    """
    df = pd.read_csv(list_csv_path)
    details = []

    for _, row in df.iterrows():
        link = row.get("link")
        if not pd.isna(link):
            try:
                detail = parse_detail(link)
                details.append(detail)
                random_sleep(0.5, 1.5)
            except Exception as e:
                logger.error(f"Error en {link}: {e}")

    df_details = pd.DataFrame(details)
    df_final = df.merge(df_details, left_on="link", right_on="url", how="left")
    df_final.to_csv("data/cortes_bogota_detailed.csv", index=False, encoding="utf-8")
    logger.success(f"Guardado {len(df_final)} registros detallados en data/cortes_bogota_detailed.csv")

if __name__ == "__main__":
    logger.add("logs/detail_scraper_{time}.log", rotation="1 MB")
    run()
