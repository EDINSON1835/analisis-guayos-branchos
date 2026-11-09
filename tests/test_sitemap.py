from guayos.sitemap import extraer_locs, filtrar_guayos

XML = """<urlset>
<url><loc>https://www.tiendasbranchos.com/adidas-guayos-predator-club-fg-niÃ±os-fucsia-66646/p</loc></url>
<url><loc>https://www.tiendasbranchos.com/fila-guayos-ria-fg-hombre-negro-61272/p</loc></url>
<url><loc>https://www.tiendasbranchos.com/camiseta-fila-hombre-1/p</loc></url>
</urlset>"""


def test_corrige_codificacion():
    locs = extraer_locs(XML)
    assert "Ã" not in "".join(locs)
    assert any("ni%C3%B1os" in u for u in locs)


def test_filtra_solo_guayos():
    guayos = filtrar_guayos(extraer_locs(XML))
    assert len(guayos) == 2
    assert all("guayos" in u for u in guayos)
