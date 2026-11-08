# Análisis de precios y descuentos de guayos – Tiendas Branchos

Proyecto académico de **Programación para Análisis de Datos** (IU Digital de Antioquia). Continúa la Evidencia de Aprendizaje 1
(extracción de datos con Selenium) y agrega control de versiones con Git y GitHub y un flujo DevOps con GitHub Actions:
pruebas automáticas (CI) y despliegue continuo (CD) de un informe web en GitHub Pages.

**Informe web desplegado:** `https://<tu-usuario>.github.io/analisis-guayos-branchos/` <!-- reemplazar -->

## Qué hace

1. Lee el `sitemap.xml` de la tienda y selecciona las páginas de producto de guayos permitidas por el `robots.txt`.
2. Visita cada página con **Selenium** (Chrome sin interfaz) y extrae SKU, nombre, marca, precio de lista, precio final, descuento y disponibilidad.
3. Calcula el descuento y el precio promedio por marca y ubica un artículo de referencia (Fila Guayos Ria Fg Hombre Negro, ref. 61272).
4. Genera un informe web estático con los resultados.

## Estructura

```
src/guayos/        parser.py, robots.py, sitemap.py, scraper.py, analysis.py, site.py
scripts/           run_scraper.py (extracción), build_site.py (informe web)
tests/             pruebas automáticas con pytest (datos de ejemplo, sin acceder a la tienda)
data/              CSV con los productos extraídos
notebooks/         cuaderno de Colab de la EA1
docs/              guía de Git, flujo DevOps y evidencias
.github/workflows/ ci.yml (pruebas) y deploy-pages.yml (despliegue)
```

## Instalación y uso

```bash
python -m venv .venv && source .venv/bin/activate      # en Windows: .venv\Scripts\activate
pip install -r requirements-dev.txt

pytest                                                  # pruebas
python scripts/run_scraper.py --limite 10               # extracción de prueba (requiere Chrome)
python scripts/build_site.py                            # genera site/index.html desde data/
```

## Flujo de trabajo con Git

- `main` es la rama estable y es la que se despliega. No se trabaja directamente sobre ella.
- Cada cambio se hace en una rama (`feature/...`, `fix/...`, `docs/...`) y llega a `main` mediante un **pull request** que debe pasar el CI.
- Mensajes de commit con prefijo: `feat:`, `fix:`, `test:`, `ci:`, `docs:`, `chore:`.
- Los hitos se marcan con etiquetas (`v1.0.0`). Detalle en [docs/guia-git.md](docs/guia-git.md).

## CI/CD

| Flujo | Cuándo corre | Qué hace |
|---|---|---|
| `ci.yml` | push a `main`/`develop` y cada pull request | instala dependencias, revisa el código con ruff y ejecuta pytest en Python 3.11 y 3.12 |
| `deploy-pages.yml` | push a `main` (si cambian código o datos) o ejecución manual | ejecuta las pruebas, construye el informe web desde `data/` y lo publica en GitHub Pages |

Explicación completa en [docs/flujo-devops.md](docs/flujo-devops.md).

## Ética y legalidad de la extracción

- Se revisa el `robots.txt` (con soporte de comodines) y solo se visitan páginas permitidas; no se recorre el listado paginado.
- Pausas de 2 s entre solicitudes y un User-Agent que identifica el uso académico.
- No se extraen datos personales. Los precios son los publicados en el momento de la extracción.
- Los flujos de GitHub Actions **no** ejecutan el scraping: el despliegue usa el CSV ya versionado.

## Autoría

Edinson Mena Arroyo · Ingeniería de Software y Datos · IU Digital de Antioquia · 2026-02
