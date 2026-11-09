import pytest

from guayos.robots import coincide, leer_grupos, url_permitida

ROBOTS = """
User-agent: *
Disallow: /checkout
Disallow: /home

User-agent: Googlebot
Allow: /cyberdays/*

User-agent: Googlebot-image
Allow: /cyberdays/*

# Disallow URL Parameters
Disallow: /*?*map*
Disallow: /*?*ft*
Disallow: /*?*page*
"""

LISTADO = "https://www.tiendasbranchos.com/guayos?map=ft&page=3"
PRODUCTO = "https://www.tiendasbranchos.com/fila-guayos-ria-fg-hombre-negro-61272/p"


def test_grupos():
    assert [ag for ag, _ in leer_grupos(ROBOTS)] == [["*"], ["googlebot"], ["googlebot-image"]]


def test_listado_con_parametros_no_permitido_en_lectura_conservadora():
    assert url_permitida(LISTADO, ROBOTS) is False


def test_pagina_de_producto_permitida():
    assert url_permitida(PRODUCTO, ROBOTS) is True


def test_regla_de_prefijo():
    assert url_permitida("https://www.tiendasbranchos.com/checkout/cart", ROBOTS) is False


@pytest.mark.parametrize("patron,ruta,esperado", [
    ("/*?*page*", "/guayos?map=ft&page=3", True),
    ("/*?*page*", "/guayos", False),
    ("/a$", "/a", True),
    ("/a$", "/ab", False),
])
def test_comodines(patron, ruta, esperado):
    assert coincide(patron, ruta) is esperado
