# scraper/utils.py
import os
import time
import random
import requests
from retrying import retry #type: ignore
from loguru import logger
from dotenv import load_dotenv

load_dotenv()

DATA_DIR = os.getenv("DATA_DIR", "./data")
DB_PATH = os.getenv("DB_PATH", os.path.join(DATA_DIR, "cortes.db"))
LOG_DIR = os.getenv("LOG_DIR", "./logs")

os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(LOG_DIR, exist_ok=True)

DEFAULT_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/120 Safari/537.36"
}

logger.add(os.path.join(LOG_DIR, "scraper_{time}.log"), rotation="5 MB")

def random_sleep(a=0.3, b=1.0):
    time.sleep(random.uniform(a, b))

@retry(stop_max_attempt_number=3, wait_fixed=2000)
def get(url, params=None, headers=None, timeout=15):
    h = headers or DEFAULT_HEADERS
    r = requests.get(url, params=params, headers=h, timeout=timeout)
    r.raise_for_status()
    return r
