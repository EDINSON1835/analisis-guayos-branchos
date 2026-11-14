"""Construye el informe web estático desde el CSV de productos.

Uso:  python scripts/build_site.py --entrada data/dataset_guayos_selenium.csv --salida site
"""
import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from guayos.site import construir_sitio  # noqa: E402


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--entrada", default="data/dataset_guayos_selenium.csv")
    ap.add_argument("--salida", default="site")
    args = ap.parse_args()
    if not Path(args.entrada).exists():
        sys.exit(f"No existe {args.entrada}. Copia ahí el CSV exportado desde el cuaderno de Colab.")
    print("Sitio generado en", construir_sitio(args.entrada, args.salida))


if __name__ == "__main__":
    main()
