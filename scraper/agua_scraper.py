from scraper.list_scraper import get_article_links
from scraper.detail_scraper import extract_article_details
import pandas as pd #type: ignore
import os

def scrape_all():
    links = get_article_links()
    all_data = []

    for link in links:
        details = extract_article_details(link)
        all_data.extend(details)

    os.makedirs("data", exist_ok=True)
    df = pd.DataFrame(all_data)
    df.to_csv("data/cortes_agua_bogota.csv", index=False, encoding="utf-8-sig")

if __name__ == "__main__":
    scrape_all()
