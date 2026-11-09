import pandas as pd

from guayos.site import construir_html, construir_sitio

DF = pd.DataFrame({
    "sku": ["1", "2"],
    "nombre": ["Marca <A> uno", "Marca B dos"],
    "marca": ["Marca", "Marca"],
    "precio_lista": [200000, 100000],
    "precio_final": [100000, 80000],
    "descuento_pct": [50, 20],
    "disponible": [True, True],
    "url": ["https://ejemplo/1/p", "https://ejemplo/2/p"],
})


def test_html_escapa_y_formatea():
    html = construir_html(DF)
    assert "&lt;A&gt;" in html          # escapa HTML del nombre
    assert "$ 100.000" in html          # formato de pesos colombianos
    assert "35.0 %" in html             # descuento promedio


def test_construir_sitio(tmp_path):
    csv = tmp_path / "datos.csv"
    DF.to_csv(csv, index=False)
    destino = construir_sitio(csv, tmp_path / "site")
    assert destino.exists()
    assert (tmp_path / "site" / ".nojekyll").exists()
