"""Ejecuta la extracción completa con Selenium y guarda el CSV.

Uso:  python scripts/run_scraper.py --limite 10 --salida data/dataset_guayos_selenium.csv
Respeta el robots.txt (solo visita URLs permitidas) y usa pausas entre solicitudes.
"""
import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from guayos.analysis import evaluar, limpiar  # noqa: E402
from guayos.scraper import scrape_selenium  # noqa: E402
from guayos.sitemap import obtener_urls_guayos  # noqa: E402


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--limite", type=int, default=None, help="máximo de páginas (prueba rápida)")
    ap.add_argument("--salida", default="data/dataset_guayos_selenium.csv")
    args = ap.parse_args()

    urls, total, guayos = obtener_urls_guayos()
    print(f"Sitemap: {total} productos, {guayos} de guayos, {len(urls)} permitidos")
    if args.limite:
        urls = urls[: args.limite]
    df, tiempo, fallos = scrape_selenium(urls)
    df = limpiar(df)
    Path(args.salida).parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(args.salida, index=False, encoding="utf-8-sig")
    print(evaluar(df, len(urls), tiempo, fallos))


if __name__ == "__main__":
    main()
