"""Lectura de una página de producto de Tiendas Branchos (HTML ya renderizado).

Extrae SKU, nombre, marca, precio de lista, precio final, descuento y disponibilidad.
"""
import re, json
from bs4 import BeautifulSoup

PATRON_PRECIO = re.compile(r"\$\s*(\d{1,3}(?:\.\d{3})+)(?:,\d{1,2})?")
PATRON_LISTPRICE = re.compile(r'"[Ll]ist[Pp]rice"\s*:\s*"?([\d\.]+)')

def a_numero(txt):
    return int(txt.replace(".", ""))

def parsear_pagina_producto(html, url):
    # Convierte el HTML de una página de producto en un diccionario (o None si no hay datos).
    soup = BeautifulSoup(html, "lxml")

    # 1) Datos estructurados (JSON-LD), antes de quitar los scripts
    nombre_ld, precio_ld, disponible = None, None, None
    for s in soup.select('script[type="application/ld+json"]'):
        try:
            datos = json.loads(s.string or "")
        except json.JSONDecodeError:
            continue
        for d in (datos if isinstance(datos, list) else [datos]):
            if isinstance(d, dict) and d.get("@type") == "Product":
                nombre_ld = d.get("name")
                ofertas = d.get("offers") or {}
                if isinstance(ofertas, list):
                    ofertas = ofertas[0] if ofertas else {}
                precio_ld = ofertas.get("lowPrice") or ofertas.get("price")
                interno = (ofertas.get("offers") or [{}])
                interno = interno[0] if isinstance(interno, list) and interno else {}
                disp = ofertas.get("availability") or interno.get("availability")
                if disp:
                    disponible = "InStock" in str(disp)

    # 2) Texto visible (sin scripts ni estilos)
    for t in soup(["script", "style", "noscript"]):
        t.decompose()
    texto = re.sub(r"\s+", " ", soup.get_text(" ", strip=True))
    h1 = soup.select_one("h1")
    nombre = h1.get_text(" ", strip=True) if h1 else nombre_ld
    ref = re.search(r"Referencia:\s*(\d+)", texto) or re.search(r"SKU:\s*(\d+)", texto)

    visibles = [a_numero(p) for p in PATRON_PRECIO.findall(texto)[:3]]
    listas_json = [int(float(x)) for x in PATRON_LISTPRICE.findall(html) if x.strip(".")]
    pcts = [int(x) for x in re.findall(r"-\s*(\d{1,2})\s*%", texto)]   # insignia de descuento

    if not nombre or not ref or (not visibles and not precio_ld):
        return None

    # 3) Precio final y candidatos a precio de lista
    if precio_ld:
        final = int(round(float(precio_ld)))
        candidatos = visibles + listas_json
    elif (len(visibles) > 1 and visibles[0] > visibles[1] and pcts
          and any(abs(int((1 - visibles[1] / visibles[0]) * 100) - p) <= 2 for p in pcts)):
        final, candidatos = visibles[1], [visibles[0]]      # par lista/final coherente con la insignia
    else:
        final, candidatos = visibles[0], []

    # 4) Precio de lista: el primer candidato mayor que el final y coherente con la insignia
    lista, descuento = final, 0
    for c in candidatos:
        if c > final and c <= final * 4:
            calc = int((1 - final / c) * 100)
            coincide = [p for p in pcts if abs(calc - p) <= 2]
            if coincide or not pcts:
                lista, descuento = c, (coincide[0] if coincide else calc)
                break

    return {
        "sku": ref.group(1),
        "nombre": nombre,
        "marca": nombre.split()[0],
        "precio_lista": lista,
        "precio_final": final,
        "descuento_pct": descuento,
        "disponible": disponible,
        "url": url,
    }
