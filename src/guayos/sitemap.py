"""Lectura del sitemap de la tienda y filtrado de las páginas de guayos."""
import re
import time
from urllib.parse import quote

import requests

from .robots import url_permitida

BASE_SITIO = "https://www.tiendasbranchos.com"
UA = "EA1-IUDigital (Edinson Mena; uso academico)"
HEADERS = {"User-Agent": UA}


def arreglar_texto(u):
    """Corrige direcciones mal decodificadas («niÃ±os» -> «niños») y las deja escapadas."""
    if "Ã" in u:
        try:
            u = u.encode("latin-1").decode("utf-8")
        except (UnicodeEncodeError, UnicodeDecodeError):
            pass
    return quote(u, safe=":/?&=%")


def extraer_locs(xml_texto):
    return [arreglar_texto(u) for u in re.findall(r"<loc>\s*(.*?)\s*</loc>", xml_texto)]


def filtrar_guayos(urls):
    return sorted({u for u in urls if "guayos" in u.lower() and u.rstrip("/").endswith("/p")})


def leer_sitemap(url):
    resp = requests.get(url, headers=HEADERS, timeout=30)
    resp.raise_for_status()
    return extraer_locs(resp.content.decode("utf-8", errors="replace"))  # el sitemap es UTF-8


def obtener_urls_guayos(pausa=2):
    """Devuelve (urls_permitidas, total_en_sitemap, total_guayos)."""
    robots = requests.get(BASE_SITIO + "/robots.txt", headers=HEADERS, timeout=20).text
    indice = leer_sitemap(BASE_SITIO + "/sitemap.xml")
    todas = []
    for sub in [u for u in indice if "/sitemap/product-" in u]:
        todas += leer_sitemap(sub)
        time.sleep(pausa)
    guayos = filtrar_guayos(todas)
    return [u for u in guayos if url_permitida(u, robots)], len(todas), len(guayos)
