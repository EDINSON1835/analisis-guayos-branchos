import pytest

from guayos.parser import parsear_pagina_producto

LD = (
    '<script type="application/ld+json">{"@type":"Product","name":"Fila Guayos Ria Fg Hombre Negro",'
    '"offers":{"@type":"AggregateOffer","lowPrice":119200,'
    '"offers":[{"price":119200,"availability":"http://schema.org/InStock"}]}}</script>'
)

CASOS = {
    "ld_visible_e_insignia": (
        f'<head>{LD}<style>.a{{margin-left:-2%}}</style></head><body><h1>Fila Guayos Ria Fg Hombre Negro</h1>'
        "<span>-40%</span><p>Referencia: 61272</p><s>$ 199.000,00</s><b>$ 119.200,00</b></body>",
        (199000, 119200, 40),
    ),
    "ld_lista_solo_en_json_de_estado": (
        f'<head>{LD}<script>var __STATE__={{"ListPrice":199000,"Price":119200}}</script></head>'
        "<body><h1>Fila Guayos Ria Fg Hombre Negro</h1><span>-40%</span><p>Referencia: 61272</p>"
        "<b>$ 119.200,00</b></body>",
        (199000, 119200, 40),
    ),
    "sin_ld_par_visible": (
        "<body><h1>Fila</h1><span>-40%</span><p>Referencia: 61272</p><s>$ 199.000,00</s><b>$ 119.200,00</b></body>",
        (199000, 119200, 40),
    ),
    "sin_descuento_y_precio_ajeno": (
        "<body><h1>Nike Guayos X</h1><p>Referencia: 9</p><b>$ 259.000,00</b><p>otros $ 80.000,00</p></body>",
        (259000, 259000, 0),
    ),
    "sin_descuento": (
        "<body><h1>Treme Guayos</h1><p>Referencia: 7</p><b>$ 149.000,00</b></body>",
        (149000, 149000, 0),
    ),
    "ld_sin_insignia_ni_lista": (
        f"<head>{LD}</head><body><h1>Fila</h1><p>Referencia: 61272</p><b>$ 119.200,00</b></body>",
        (119200, 119200, 0),
    ),
}


@pytest.mark.parametrize("nombre", list(CASOS))
def test_precios_y_descuento(nombre):
    html, (lista, final, desc) = CASOS[nombre]
    r = parsear_pagina_producto(html, "https://ejemplo/p")
    assert (r["precio_lista"], r["precio_final"], r["descuento_pct"]) == (lista, final, desc)


def test_campos_basicos():
    r = parsear_pagina_producto(CASOS["ld_visible_e_insignia"][0], "https://ejemplo/p")
    assert r["sku"] == "61272"
    assert r["marca"] == "Fila"
    assert r["disponible"] is True
    assert r["url"] == "https://ejemplo/p"


def test_pagina_sin_datos_devuelve_none():
    assert parsear_pagina_producto("<html><body><p>Cargando...</p></body></html>", "u") is None
