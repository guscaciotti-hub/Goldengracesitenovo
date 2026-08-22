#!/usr/bin/env python3
"""
Gera assets/og.png (1200x630) — o cartão que aparece quando o link é
compartilhado no WhatsApp, que é como esse público repassa link.

Layout: oferta à esquerda, o lineup real dos frascos à direita, e a faixa
preta do lucro embaixo. Rode depois de tools/preparar-imagens.py.
"""

import io
import pathlib

from PIL import Image, ImageDraw
from fontTools.ttLib import TTFont

RAIZ = pathlib.Path(__file__).resolve().parent.parent
FONTES = RAIZ / "assets" / "fonts"
DESTINO = RAIZ / "assets" / "og.png"

INK = (17, 17, 17)
GOLD = (200, 155, 95)
PAPER = (255, 255, 255)
CINZA = (185, 185, 185)

L, A = 1200, 630
MARGEM = 70
FAIXA = 452


def carregar(nome_woff2: str, tamanho: int):
    """Descompacta o woff2 em memória e devolve a fonte no tamanho pedido."""
    fonte = TTFont(FONTES / nome_woff2, fontNumber=0)
    buffer = io.BytesIO()
    fonte.flavor = None
    fonte.save(buffer)
    buffer.seek(0)
    return ImageFontTruetype(buffer, tamanho)


def ImageFontTruetype(buf, tamanho):
    from PIL import ImageFont
    return ImageFont.truetype(buf, tamanho)


def centralizar(d, y, texto, fonte, cor, x0=0, x1=L):
    caixa = d.textbbox((0, 0), texto, font=fonte)
    d.text((x0 + (x1 - x0 - (caixa[2] - caixa[0])) / 2 - caixa[0], y), texto, font=fonte, fill=cor)


def main() -> None:
    tela = Image.new("RGB", (L, A), PAPER)
    d = ImageDraw.Draw(tela)

    serif_lg = carregar("playfair-latin.woff2", 78)
    serif_md = carregar("playfair-latin.woff2", 44)
    serif_faixa = carregar("playfair-latin.woff2", 60)
    sans = carregar("plex-latin.woff2", 23)

    # ── produto real à direita, alinhado pela base do bloco branco ──
    lineup = Image.open(RAIZ / "assets" / "hero-composicao.webp").convert("RGBA")
    largura = 470
    lineup = lineup.resize((largura, round(lineup.height * largura / lineup.width)), Image.LANCZOS)
    tela.paste(lineup, (L - largura - MARGEM + 20, FAIXA - lineup.height - 14), lineup)

    # ── logo oficial ──
    logo = Image.open(RAIZ / "assets" / "logo.webp").convert("RGBA")
    lw = 230
    logo = logo.resize((lw, round(logo.height * lw / logo.width)), Image.LANCZOS)
    tela.paste(logo, (MARGEM, 66), logo)

    # ── oferta ──
    d.text((MARGEM, 146), "Kit Vitrine", font=serif_lg, fill=INK)
    d.text((MARGEM, 252), "5 unidades por R$ 169", font=serif_md, fill=INK)
    d.text((MARGEM, 330), "Você não paga nada agora.", font=sans, fill=INK)
    d.text((MARGEM, 364), "Paga na entrega, na sua loja.", font=sans, fill=(95, 95, 95))

    # ── faixa do lucro ──
    d.rectangle([0, FAIXA, L, A], fill=INK)
    centralizar(d, 486, "LUCRO POR KIT", sans, CINZA)
    centralizar(d, 522, "R$ 230", serif_faixa, GOLD)

    tela.save(DESTINO, "PNG", optimize=True)
    print(f"assets/og.png  {DESTINO.stat().st_size // 1024} KB")


if __name__ == "__main__":
    main()
