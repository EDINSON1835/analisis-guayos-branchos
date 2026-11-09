import pandas as pd
import pytest

from guayos.analysis import evaluar, limpiar, resumen_por_marca, ubicar_ancla

# Datos SINTÉTICOS solo para probar las funciones (no son datos de la tienda).
DF = pd.DataFrame({
    "sku": ["1", "2", "3", "3", "4"],
    "nombre": ["A x", "A y", "B z", "B z", "B w"],
    "marca": ["A", "A", "B", "B", "B"],
    "precio_lista": [200, 100, 300, 300, 400],
    "precio_final": [100, 80, 150, 150, 300],
    "descuento_pct": [50, 20, 50, 50, 25],
    "disponible": [True, True, True, True, None],
    "url": ["u1", "u2", "u3", "u3", "u4"],
})


def test_limpiar_quita_duplicados():
    assert len(limpiar(DF)) == 4


def test_resumen_por_marca():
    r = resumen_por_marca(limpiar(DF))
    assert r.loc["A", "productos"] == 2
    assert r.loc["A", "descuento_prom"] == 35.0
    assert r.loc["B", "precio_max"] == 300


def test_ubicar_ancla():
    d = limpiar(DF)
    r = ubicar_ancla(d, "2")
    assert r["descuento"] == 20
    assert r["descuento_marca"] == 35.0
    assert r["descuento_catalogo"] == pytest.approx(36.2, abs=0.1)
    assert ubicar_ancla(d, "999") is None


def test_evaluar():
    d = limpiar(DF)
    m = evaluar(d, intentadas=5, tiempo_s=50, fallos=1)
    assert m["productos_extraidos"] == 4
    assert m["cobertura_pct"] == 80.0
    assert m["segundos_por_pagina"] == 10.0
    assert m["completitud_pct"] == 100.0
