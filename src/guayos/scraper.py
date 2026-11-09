"""Extracción con Selenium (Chrome headless) de las páginas de producto."""
import random
import time

import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from .parser import parsear_pagina_producto
from .sitemap import UA


def crear_driver():
    op = Options()
    op.page_load_strategy = "eager"  # no espera imágenes ni anuncios: evita cuelgues
    for arg in ["--headless=new", "--no-sandbox", "--disable-dev-shm-usage", "--disable-gpu",
                "--disable-extensions", "--window-size=1366,2000", f"--user-agent={UA}"]:
        op.add_argument(arg)
    d = webdriver.Chrome(options=op)
    d.set_page_load_timeout(40)
    d.set_script_timeout(40)
    return d


def scrape_selenium(urls, pausa=2, espera_carga=1.5, progreso=True):
    """Visita cada URL y devuelve (DataFrame, tiempo_total_s, fallos)."""
    filas, fallos = [], 0
    t0 = time.time()
    driver = crear_driver()
    try:
        for i, u in enumerate(urls, 1):
            try:
                driver.get(u)
                WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.TAG_NAME, "h1")))
                time.sleep(espera_carga)
                item = parsear_pagina_producto(driver.page_source, u)
                if item:
                    filas.append(item)
                else:
                    fallos += 1
            except Exception as e:  # incluye timeouts de Selenium y de urllib3
                fallos += 1
                print(f"[Selenium] error en {u}: {type(e).__name__}")
                try:
                    driver.quit()
                except Exception:
                    pass
                driver = crear_driver()
            if progreso and i % 10 == 0:
                print(f"[Selenium] {i}/{len(urls)} páginas")
            time.sleep(pausa + random.random() * 0.5)
    finally:
        try:
            driver.quit()
        except Exception:
            pass
    return pd.DataFrame(filas), time.time() - t0, fallos
