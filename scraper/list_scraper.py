# scraper/list_scraper.py
from bs4 import BeautifulSoup
import pandas as pd # type: ignore
from urllib.parse import urljoin
from scraper.utils import get, random_sleep, logger
import os

BASE = os.getenv("BASE_URL", "https://bogota.gov.co/tag/cortes-de-luz-en-bogota")

def parse_list_page(html, base_url="https://bogota.gov.co"):
    soup = BeautifulSoup(html, "html.parser")
    # SELECTOR a validar en DevTools:
    # intento con contenedores de artículo tipo Drupal: div.node--type-article
    article_nodes = soup.select("div.node--type-article")
    results = []
    for node in article_nodes:
        # título y link
        a = node.select_one("h2 a")
        title = a.get_text(strip=True) if a else None
        link = a["href"] if a and a.has_attr("href") else None
        if link and link.startswith("/"):
            link = urljoin(base_url, link)
        # fecha (tiempo)
        time_el = node.select_one("time")
        pubdate = time_el.get_text(strip=True) if time_el else None
        results.append({"title": title, "link": link, "pubdate": pubdate})
    return results

def scrape_list_pages(pages=5):
    all_items = []
    for p in range(1, pages + 1):
        if p == 1:
            url = BASE
        else:
            url = f"{BASE}/page/{p}"
        logger.info(f"Scraping listado: {url}")
        try:
            resp = get(url)
            items = parse_list_page(resp.text)
            if not items:
                logger.info("No se encontraron items en la página, interrumpiendo paginación.")
                break
            all_items.extend(items)
            random_sleep(0.5, 1.2)
        except Exception as e:
            logger.error(f"Error scrappeando {url}: {e}")
            break
    df = pd.DataFrame(all_items).drop_duplicates(subset=["link"])
    out = os.path.join(os.getenv("DATA_DIR", "./data"), "cortes_bogota_listado.csv")
    df.to_csv(out, index=False, encoding="utf-8")
    logger.info(f"Guardado listado: {out} ({len(df)} registros)")
    return df

if __name__ == "__main__":
    scrape_list_pages(pages=6)
