"""Análisis descriptivo de los productos extraídos."""
import pandas as pd  # noqa: F401

CAMPOS = ["sku", "nombre", "marca", "precio_lista", "precio_final", "descuento_pct"]


def limpiar(df):
    """Elimina duplicados por SKU y deja el SKU como texto."""
    out = df.copy()
    out["sku"] = out["sku"].astype(str)
    return out.drop_duplicates("sku").reset_index(drop=True)


def resumen_por_marca(df):
    return (df.groupby("marca")
              .agg(productos=("sku", "count"),
                   descuento_prom=("descuento_pct", "mean"),
                   precio_final_prom=("precio_final", "mean"),
                   precio_min=("precio_final", "min"),
                   precio_max=("precio_final", "max"))
              .round(1)
              .sort_values("productos", ascending=False))


def ubicar_ancla(df, sku):
    """Compara el descuento del artículo ancla con su marca y con el catálogo."""
    fila = df[df["sku"].astype(str) == str(sku)]
    if fila.empty:
        return None
    a = fila.iloc[0]
    marca = df[df["marca"] == a["marca"]]
    return {
        "nombre": a["nombre"],
        "descuento": int(a["descuento_pct"]),
        "descuento_marca": round(float(marca["descuento_pct"].mean()), 1),
        "descuento_catalogo": round(float(df["descuento_pct"].mean()), 1),
        "percentil": round(float((df["descuento_pct"] < a["descuento_pct"]).mean() * 100)),
        "precio_final": int(a["precio_final"]),
        "precio_max_marca": int(marca["precio_final"].max()),
    }


def evaluar(df, intentadas, tiempo_s, fallos):
    """Métricas de la extracción: cobertura, tiempo, completitud y errores."""
    completos = int(df[CAMPOS].notna().all(axis=1).sum())
    return {
        "paginas_intentadas": intentadas,
        "productos_extraidos": len(df),
        "cobertura_pct": round(len(df) / intentadas * 100, 1) if intentadas else 0.0,
        "tiempo_total_s": round(tiempo_s, 1),
        "segundos_por_pagina": round(tiempo_s / intentadas, 2) if intentadas else 0.0,
        "sin_dato_o_error": fallos,
        "completitud_pct": round(completos / max(len(df), 1) * 100, 1),
    }
