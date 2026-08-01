#!/usr/bin/env python3
"""
Gera uma versão de arquivo único da página, com fontes e imagens embutidas
como data URI. Serve para pré-visualizar num link, sem servidor.

O site de verdade é o index.html + /assets — este arquivo é só um espelho.
"""

import base64
import pathlib
import re
import sys

RAIZ = pathlib.Path(__file__).resolve().parent.parent
SAIDA = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else RAIZ / "preview-arquivo-unico.html"

html = (RAIZ / "index.html").read_text(encoding="utf-8")


def data_uri(caminho: pathlib.Path, mime: str) -> str:
    return f"data:{mime};base64," + base64.b64encode(caminho.read_bytes()).decode()


# fontes
for nome in ("playfair-latin", "inter-latin"):
    html = html.replace(
        f"url(assets/fonts/{nome}.woff2)",
        f"url({data_uri(RAIZ / 'assets/fonts' / f'{nome}.woff2', 'font/woff2')})",
    )

# frascos
for svg in sorted((RAIZ / "assets").glob("rotulo-*.svg")):
    html = html.replace(f'src="assets/{svg.name}"', f'src="{data_uri(svg, "image/svg+xml")}"')

# favicon
html = html.replace(
    'href="assets/favicon.svg"', f'href="{data_uri(RAIZ / "assets/favicon.svg", "image/svg+xml")}"'
)

# preload não faz sentido com data URI
html = re.sub(r'\s*<link rel="preload"[^>]*>', "", html)

SAIDA.parent.mkdir(parents=True, exist_ok=True)
SAIDA.write_text(html, encoding="utf-8")
restantes = re.findall(r"assets/(?!fonts)[\w.-]+", html)
print(f"{SAIDA}  {SAIDA.stat().st_size} bytes")
print("referências externas restantes:", sorted(set(restantes)) or "nenhuma")
