#!/usr/bin/env python3
"""
Processa os arquivos originais em assets/originais/ e gera o que a página usa.

As cinco fotos vieram do mesmo rig: fundo #ECEAEB liso nos quatro cantos e o
frasco exatamente no mesmo lugar em todas. Isso permite recortar as cinco com
o mesmo enquadramento e montar o lineup do hero sem máscara e sem emenda —
basta colar sobre um fundo da mesma cor.

Rode de novo só se trocar as fotos originais.
"""

import pathlib

from PIL import Image, ImageDraw

RAIZ = pathlib.Path(__file__).resolve().parent.parent
ORIG = RAIZ / "assets" / "originais"
ASSETS = RAIZ / "assets"

FUNDO = (236, 234, 235)          # cor do fundo de estúdio, medida nos cantos
BBOX = (617, 1522, 312, 2933)    # x0, x1, y0, y1 do frasco — igual nas cinco

# ordem do lineup: quente, frio, dourado no centro, frio, quente
FRAGRANCIAS = [
    ("sweet-reign",    "ROTULO Sweet Reign - EMBALAGEM.jpg"),
    ("midnight-grace", "ROTULO Midnight Grace - EMBALAGEM.jpg"),
    ("golden-aura",    "ROTULO Golden Aura - EMBALAGEM.jpg"),
    ("azure-mist",     "ROTULO Azure Mist - EMBALAGEM.jpg"),
    ("royal-bloom",    "ROTULO ROYAL BLOOM - EMBALAGEM.jpg"),
]


def sem_fundo(im: Image.Image) -> Image.Image:
    """
    Tira o fundo de estúdio por inundação a partir das bordas. Chave de cor
    global comeria as partes claras do vidro; a inundação só remove o fundo
    contíguo e preserva o que está fechado dentro do frasco.
    """
    im = im.convert("RGBA")
    w, h = im.size
    bordas = [(0, 0), (w - 1, 0), (0, h - 1), (w - 1, h - 1),
              (w // 2, 0), (w // 2, h - 1), (0, h // 2), (w - 1, h // 2)]
    for ponto in bordas:
        ImageDraw.floodfill(im, ponto, (0, 0, 0, 0), thresh=22)
    return im


def recorte_do_card(im: Image.Image) -> Image.Image:
    """Recorta em 2:3 centrado no frasco, com folga em cima e embaixo."""
    x0, x1, y0, y1 = BBOX
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    altura = 2900
    largura = round(altura * 2 / 3)
    caixa = (round(cx - largura / 2), round(cy - altura / 2),
             round(cx + largura / 2), round(cy + altura / 2))
    return sem_fundo(im).crop(caixa).resize((667, 1000), Image.LANCZOS)


def recorte_da_mini(im: Image.Image) -> Image.Image:
    """
    Miniatura da lista de pedido: o frasco inteiro, enquadrado justo.

    O recorte do card tem folga de sobra porque lá a foto ocupa a largura de
    uma coluna. Na linha do pedido ela tem 48px — com a mesma folga o frasco
    viraria um risco no meio de um retângulo vazio. Aqui a margem é só a
    necessária para o vidro não encostar na borda do azulejo.
    """
    x0, x1, y0, y1 = BBOX
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    largura = round((x1 - x0) * 1.22)
    altura = round((y1 - y0) * 1.05)
    caixa = (round(cx - largura / 2), round(cy - altura / 2),
             round(cx + largura / 2), round(cy + altura / 2))
    cortado = sem_fundo(im).crop(caixa)
    final_l = 140
    return cortado.resize((final_l, round(cortado.height * final_l / cortado.width)), Image.LANCZOS)


def frasco_recortado(im: Image.Image) -> Image.Image:
    """Só o frasco, já sem fundo, aparado no próprio contorno."""
    recortado = sem_fundo(im)
    return recortado.crop(recortado.getbbox())


def montar_lineup(frascos: list[Image.Image]) -> Image.Image:
    """
    Cinco frascos em arco, o do centro maior e mais à frente. Com fundo
    transparente dá para sobrepor de verdade, e o grupo fica junto em vez de
    parecer cinco fotos enfileiradas.
    """
    larg, alt = 2000, 1400
    tela = Image.new("RGBA", (larg, alt), (0, 0, 0, 0))

    escalas = [0.86, 0.94, 1.00, 0.94, 0.86]
    base = [1100, 1130, 1160, 1130, 1100]   # linha de base: centro mais baixo = mais perto
    altura_ref = 1020

    redimensionados = []
    for f, e in zip(frascos, escalas):
        h = round(altura_ref * e)
        w = round(f.width * h / f.height)
        redimensionados.append(f.resize((w, h), Image.LANCZOS))

    # sobreposição: aproxima os frascos sem esconder rótulo
    passo = [round(f.width * 0.82) for f in redimensionados]
    total = sum(passo[:-1]) + redimensionados[-1].width
    x = (larg - total) // 2

    # os de trás entram primeiro, o do centro por cima
    ordem = [0, 4, 1, 3, 2]
    posicoes = []
    cursor = x
    for i, f in enumerate(redimensionados):
        posicoes.append(cursor)
        cursor += passo[i]
    for i in ordem:
        f = redimensionados[i]
        tela.alpha_composite(f, (posicoes[i], base[i] - f.height))

    tela = tela.crop(tela.getbbox())
    larg_final = 1000
    return tela.resize((larg_final, round(tela.height * larg_final / tela.width)), Image.LANCZOS)


def preparar_logo(origem: pathlib.Path, destino: pathlib.Path, claro: bool = False) -> None:
    """Apara a margem transparente. Na versão clara, a letra vira branca e o & segue dourado."""
    im = Image.open(origem).convert("RGBA")
    caixa = im.getbbox()
    if caixa:
        im = im.crop(caixa)
    if claro:
        px = im.load()
        for y in range(im.height):
            for x in range(im.width):
                r, g, b, a = px[x, y]
                if a == 0:
                    continue
                # o "&" é o único elemento colorido; o resto vira branco
                if max(r, g, b) - min(r, g, b) < 28:
                    px[x, y] = (255, 255, 255, a)
    largura = 900
    im = im.resize((largura, round(im.height * largura / im.width)), Image.LANCZOS)
    im.save(destino, "WEBP", quality=88, method=6)


def main() -> None:
    (ASSETS / "frascos" / "mini").mkdir(parents=True, exist_ok=True)

    frascos = []
    for slug, arquivo in FRAGRANCIAS:
        im = Image.open(ORIG / arquivo).convert("RGB")
        saida = ASSETS / "frascos" / f"{slug}.webp"
        recorte_do_card(im).save(saida, "WEBP", quality=84, method=6)
        print(f"  {saida.relative_to(RAIZ)}  {saida.stat().st_size // 1024} KB")

        mini = ASSETS / "frascos" / "mini" / f"{slug}.webp"
        recorte_da_mini(im).save(mini, "WEBP", quality=80, method=6)
        print(f"  {mini.relative_to(RAIZ)}  {mini.stat().st_size / 1024:.1f} KB")

        frascos.append(frasco_recortado(im))

    lineup = ASSETS / "hero-composicao.webp"
    montar_lineup(frascos).save(lineup, "WEBP", quality=86, method=6, lossless=False)
    print(f"  {lineup.relative_to(RAIZ)}  {lineup.stat().st_size // 1024} KB")

    preparar_logo(ORIG / "LOGO HORIZONTAL.png", ASSETS / "logo.webp")
    preparar_logo(ORIG / "LOGO HORIZONTAL.png", ASSETS / "logo-claro.webp", claro=True)
    for n in ("logo.webp", "logo-claro.webp"):
        print(f"  assets/{n}  {(ASSETS / n).stat().st_size // 1024} KB")


if __name__ == "__main__":
    main()
