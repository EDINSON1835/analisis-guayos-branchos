"""Genera el informe web estático (GitHub Pages) a partir del CSV de productos."""
from html import escape
from pathlib import Path

import pandas as pd

from .analysis import limpiar, resumen_por_marca


def _fmt(n):
    return f"$ {int(round(n)):,}".replace(",", ".")


def construir_html(df, titulo="Guayos Tiendas Branchos: precios y descuentos"):
    df = limpiar(df)
    marcas = resumen_por_marca(df)
    maximo = max(float(marcas["descuento_prom"].max()), 1.0)
    barras = "\n".join(
        f'<div class="fila"><span class="m">{escape(str(m))}</span>'
        f'<span class="b" style="width:{r.descuento_prom / maximo * 60:.0f}%"></span>'
        f'<span class="v">{r.descuento_prom:.1f} %</span></div>'
        for m, r in marcas.sort_values("descuento_prom", ascending=False).iterrows()
    )
    filas_marca = "\n".join(
        f"<tr><td>{escape(str(m))}</td><td>{int(r.productos)}</td><td>{r.descuento_prom:.1f} %</td>"
        f"<td>{_fmt(r.precio_final_prom)}</td><td>{_fmt(r.precio_min)} – {_fmt(r.precio_max)}</td></tr>"
        for m, r in marcas.iterrows()
    )
    filas_prod = "\n".join(
        f'<tr><td>{escape(str(r.sku))}</td><td><a href="{escape(str(r.url))}">{escape(str(r.nombre))}</a></td>'
        f"<td>{_fmt(r.precio_lista)}</td><td>{_fmt(r.precio_final)}</td><td>{int(r.descuento_pct)} %</td></tr>"
        for r in df.sort_values("descuento_pct", ascending=False).itertuples()
    )
    return f"""<!doctype html>
<html lang="es"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{escape(titulo)}</title>
<style>
body{{font-family:system-ui,Arial,sans-serif;max-width:960px;margin:2rem auto;padding:0 1rem;color:#1f2937}}
table{{border-collapse:collapse;width:100%;margin:1rem 0}} th,td{{border:1px solid #d1d5db;padding:.4rem .6rem;text-align:left}}
th{{background:#e5edf9}} .fila{{display:flex;align-items:center;gap:.6rem;margin:.3rem 0}}
.m{{width:6rem}} .b{{background:#2f5496;height:1.1rem;display:inline-block}} .v{{font-size:.9rem}}
.tabla{{overflow-x:auto}}
</style></head><body>
<h1>{escape(titulo)}</h1>
<p>{len(df)} productos de la categoría guayos. Proyecto académico (IU Digital de Antioquia, Programación para Análisis de Datos).
Los precios corresponden al momento de la extracción y pueden cambiar con las campañas de la tienda.</p>
<h2>Descuento promedio por marca</h2>
{barras}
<h2>Resumen por marca</h2>
<div class="tabla"><table><tr><th>Marca</th><th>Productos</th><th>Descuento prom.</th><th>Precio final prom.</th><th>Rango de precio final</th></tr>
{filas_marca}</table></div>
<h2>Productos</h2>
<div class="tabla"><table><tr><th>SKU</th><th>Producto</th><th>Precio de lista</th><th>Precio final</th><th>Descuento</th></tr>
{filas_prod}</table></div>
</body></html>
"""


def construir_sitio(csv_entrada, carpeta_salida):
    df = pd.read_csv(csv_entrada, dtype={"sku": str})
    salida = Path(carpeta_salida)
    salida.mkdir(parents=True, exist_ok=True)
    (salida / "index.html").write_text(construir_html(df), encoding="utf-8")
    (salida / ".nojekyll").write_text("", encoding="utf-8")
    return salida / "index.html"
