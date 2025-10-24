"""
utils.py
--------
Funciones utilitarias compartidas por los módulos del scraper.
"""

import time
import random
import requests
from loguru import logger

# Headers para simular un navegador
DEFAULT_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100 Safari/537.36"
}

def get(url, params=None, headers=None, timeout=15):
    """
    Envía una solicitud HTTP GET de manera segura.

    Args:
        url (str): Dirección del recurso a consultar.
        params (dict, optional): Parámetros de la URL.
        headers (dict, optional): Cabeceras HTTP.
        timeout (int): Tiempo máximo de espera.

    Returns:
        requests.Response: Respuesta del servidor.
    """
    h = headers or DEFAULT_HEADERS
    try:
        response = requests.get(url, params=params, headers=h, timeout=timeout)
        response.raise_for_status()
        return response
    except requests.RequestException as e:
        logger.error(f"Error en la solicitud GET a {url}: {e}")
        raise

def random_sleep(a=0.3, b=1.2):
    """Pausa aleatoria entre solicitudes para evitar bloqueos del servidor."""
    time.sleep(random.uniform(a, b))
