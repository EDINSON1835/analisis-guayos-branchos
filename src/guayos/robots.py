"""Verificador de robots.txt con soporte de comodines (*) y de $ al final.

urllib.robotparser no interpreta comodines, por eso se usa este verificador propio.
"""
import re
from urllib.parse import urlparse


def leer_grupos(texto):
    """Devuelve una lista de (agentes, reglas) a partir del texto de un robots.txt."""
    grupos, agentes, reglas, ultimo_agente = [], [], [], False
    for linea in texto.splitlines():
        linea = linea.split("#", 1)[0].strip()
        if ":" not in linea:
            continue
        clave, valor = [x.strip() for x in linea.split(":", 1)]
        clave = clave.lower()
        if clave == "user-agent":
            if not ultimo_agente and (agentes or reglas):
                grupos.append((agentes, reglas))
                agentes, reglas = [], []
            agentes.append(valor.lower())
            ultimo_agente = True
        elif clave in ("allow", "disallow"):
            reglas.append((clave, valor))
            ultimo_agente = False
    if agentes or reglas:
        grupos.append((agentes, reglas))
    return grupos


def coincide(patron, ruta):
    fin = patron.endswith("$")
    cuerpo = patron[:-1] if fin else patron
    regex = "^" + re.escape(cuerpo).replace(r"\*", ".*") + ("$" if fin else "")
    return re.match(regex, ruta) is not None


def permitido(url, reglas):
    """True si ninguna regla Disallow aplica (gana la regla más específica; empate: Allow)."""
    p = urlparse(url)
    ruta = p.path + ("?" + p.query if p.query else "")
    mejor = None
    for tipo, patron in reglas:
        if patron and coincide(patron, ruta):
            if mejor is None or len(patron) > len(mejor[1]) or (
                len(patron) == len(mejor[1]) and tipo == "allow"
            ):
                mejor = (tipo, patron)
    return mejor is None or mejor[0] == "allow"


def reglas_estrictas(grupos):
    """Solo las reglas del grupo User-agent: *."""
    return [r for agentes, reglas in grupos if "*" in agentes for r in reglas]


def reglas_conservadoras(grupos):
    """Reglas del grupo * más todos los Disallow del archivo, sin importar el grupo."""
    return reglas_estrictas(grupos) + [
        r for _, reglas in grupos for r in reglas if r[0] == "disallow"
    ]


def url_permitida(url, texto_robots):
    """True solo si la URL es permitida en la lectura estricta Y en la conservadora."""
    grupos = leer_grupos(texto_robots)
    return permitido(url, reglas_estrictas(grupos)) and permitido(url, reglas_conservadoras(grupos))
