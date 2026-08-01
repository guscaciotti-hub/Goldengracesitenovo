#!/usr/bin/env python3
"""Gera assets/og.png (1200x630) — a imagem que aparece quando o link
é compartilhado no WhatsApp, Instagram ou Facebook."""

import io
import pathlib

from PIL import Image, ImageDraw, ImageFont
from fontTools.ttLib import TTFont

RAIZ = pathlib.Path(__file__).resolve().parent.parent
FONTES = RAIZ / "assets" / "fonts"
DESTINO = RAIZ / "assets" / "og.png"

INK = (17, 17, 17)
GOLD = (200, 155, 95)
PAPER = (255, 255, 255)
CINZA = (185, 185, 185)


def carregar(nome_woff2: str, tamanho: int) -> ImageFont.FreeTypeFont:
    """Descompacta o woff2 para TTF em memória e devolve a fonte no tamanho pedido."""
    fonte = TTFont(FONTES / nome_woff2, fontNumber=0)
    buffer = io.BytesIO()
    fonte.flavor = None
    fonte.save(buffer)
    buffer.seek(0)
    return ImageFont.truetype(buffer, tamanho)


def centralizar(desenho, y, texto, fonte, cor, largura=1200):
    caixa = desenho.textbbox((0, 0), texto, font=fonte)
    desenho.text(((largura - (caixa[2] - caixa[0])) / 2 - caixa[0], y), texto, font=fonte, fill=cor)


def main() -> None:
    tela = Image.new("RGB", (1200, 630), PAPER)
    d = ImageDraw.Draw(tela)

    serif_lg = carregar("playfair-latin.woff2", 92)
    serif_md = carregar("playfair-latin.woff2", 64)
    serif_sm = carregar("playfair-latin.woff2", 40)
    sans_sm = carregar("inter-latin.woff2", 25)

    # faixa preta inferior com o lucro
    d.rectangle([0, 452, 1200, 630], fill=INK)

    # logo
    centralizar(d, 62, "GOLDEN", serif_sm, INK)
    caixa = d.textbbox((0, 0), "&GRACE", font=serif_sm)
    x = (1200 - (caixa[2] - caixa[0])) / 2 - caixa[0]
    d.text((x, 108), "&", font=serif_sm, fill=GOLD)
    largura_amp = d.textbbox((0, 0), "&", font=serif_sm)[2]
    d.text((x + largura_amp, 108), "GRACE", font=serif_sm, fill=INK)

    # oferta
    centralizar(d, 200, "Kit Vitrine", serif_lg, INK)
    centralizar(d, 310, "10 unidades por R$ 329", serif_md, INK)
    centralizar(d, 396, "Body splash 200 ml  ·  As 5 fragrâncias  ·  Tester incluso", sans_sm, (90, 90, 90))

    # faixa do lucro
    centralizar(d, 486, "LUCRO POR KIT", sans_sm, CINZA)
    centralizar(d, 520, "R$ 470", serif_md, GOLD)

    tela.save(DESTINO, "PNG", optimize=True)
    print(f"assets/og.png  {DESTINO.stat().st_size} bytes")


if __name__ == "__main__":
    main()
