"""
list_scraper.py
---------------
Extrae el listado de artículos sobre cortes de luz desde
https://bogota.gov.co/tag/cortes-de-luz-en-bogota
"""

import pandas as pd # type: ignore
from bs4 import BeautifulSoup
from loguru import logger
from .utils import get, random_sleep

def parse_article(article_tag):
    """
    Extrae título, enlace y fecha de un artículo del listado principal.

    Args:
        article_tag (bs4.element.Tag): bloque HTML de un artículo.

    Returns:
        dict: datos limpios con 'title', 'link', 'pubdate'.
    """
    try:
        title = article_tag.select_one("h2 a").get_text(strip=True)
    except:
        title = None

    try:
        link = article_tag.select_one("h2 a")["href"]
        if link.startswith("/"):
            link = "https://bogota.gov.co" + link
    except:
        link = None

    try:
        pubdate = article_tag.select_one("time").get_text(strip=True)
    except: 
        pubdate = None

    return {"title": title, "link": link, "pubdate": pubdate}

def scrape_page(page_url):
    """
    Descarga y analiza una página del listado.

    Args:
        page_url (str): URL de la página.

    Returns:
        list[dict]: Lista de artículos encontrados.
    """
    logger.info(f"Scrapeando página: {page_url}")
    resp = get(page_url)
    soup = BeautifulSoup(resp.text, "html.parser")
    article_tags = soup.select("div.node--type-article")

    results = [parse_article(a) for a in article_tags]
    random_sleep(0.5, 1.0)
    return results

def run():
    """Ejecuta el scraper del listado completo."""
    base_url = "https://bogota.gov.co/tag/cortes-de-luz-en-bogota"
    all_results = []

    for page in range(1, 6):  # cambia si hay más páginas
        url = base_url if page == 1 else f"{base_url}/page/{page}"
        try:
            results = scrape_page(url)
            if not results:
                break
            all_results.extend(results)
        except Exception as e:
            logger.error(f"Error procesando {url}: {e}")
            break

    df = pd.DataFrame(all_results)
    df.to_csv("data/cortes_bogota_listado.csv", index=False, encoding="utf-8")
    logger.success(f"Listado guardado con {len(df)} artículos.")

if __name__ == "__main__":
    logger.add("logs/list_scraper_{time}.log", rotation="1 MB")
    run()
