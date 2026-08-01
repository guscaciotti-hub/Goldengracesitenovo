#!/usr/bin/env python3
"""
Gera os SVGs de apoio dos frascos (assets/rotulo-*.svg).

Estes arquivos sao um stand-in vetorial da linha, na identidade da marca.
Quando as fotos reais estiverem prontas, exporte-as em WebP (max. 800px de
largura) como assets/rotulo-<slug>.webp e troque a extensao no index.html.
"""

import pathlib

RAIZ = pathlib.Path(__file__).resolve().parent.parent
DESTINO = RAIZ / "assets"

INK = "#111111"
GOLD = "#C89B5F"
GOLD_ESCURO = "#9C7638"
VIDRO = "#DCDCDC"

FRAGRANCIAS = [
    # slug,            nome,              cor do respingo
    ("sweet-reign",    "Sweet Reign",     "#C4796B"),
    ("royal-bloom",    "Royal Bloom",     "#C22B5E"),
    ("midnight-grace", "Midnight Grace",  "#1B4E9B"),
    ("azure-mist",     "Azure Mist",      "#1B8FD1"),
    ("golden-aura",    "Golden Aura",     "#C89B5F"),
]

# Fitas do respingo — onda subindo pela direita, como no rótulo. (path, espessura, opacidade)
FITAS = [
    ("M136 556 C166 549 201 526 225 481 C239 454 245 431 247 409", 16, 0.82),
    ("M151 561 C183 553 215 533 235 497", 8, 0.50),
    ("M131 548 C160 559 211 561 269 545", 9, 0.55),
    ("M146 535 C171 543 206 544 241 533", 4, 0.32),
    ("M244 401 C248 387 251 377 251 366", 4, 0.45),
]

# Gotas soltas: (cx, cy, r, opacidade)
GOTAS = [
    (253, 351, 3.2, 0.70), (243, 378, 2.2, 0.55), (259, 392, 2.0, 0.50),
    (236, 430, 1.8, 0.45), (262, 424, 2.6, 0.60), (250, 448, 1.7, 0.42),
    (224, 456, 1.5, 0.40), (266, 462, 2.2, 0.52), (210, 492, 1.8, 0.45),
    (196, 512, 1.5, 0.38), (176, 530, 1.4, 0.35), (257, 330, 2.0, 0.50),
    (240, 350, 1.5, 0.38), (264, 369, 1.4, 0.35),
]

SERIF = "Georgia,'Times New Roman','Playfair Display',serif"
SANS = "'Helvetica Neue',Helvetica,Arial,sans-serif"


def montar(slug: str, nome: str, cor: str) -> str:
    fitas = "\n".join(
        f'      <path d="{d}" stroke="{cor}" stroke-width="{w}" stroke-linecap="round" '
        f'fill="none" opacity="{o}"/>'
        for d, w, o in FITAS
    )
    gotas = "\n".join(
        f'      <circle cx="{cx}" cy="{cy}" r="{r}" fill="{cor}" opacity="{o}"/>'
        for cx, cy, r, o in GOTAS
    )
    # Estrias verticais da gola dourada
    estrias = "\n".join(
        f'    <line x1="{x}" y1="143" x2="{x}" y2="187" stroke="{GOLD_ESCURO}" '
        f'stroke-width="1.4" opacity="0.55"/>'
        for x in range(168, 240, 11)
    )

    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="120 26 160 556" width="160" height="556" role="img" aria-label="Frasco de body splash {nome}, 200 ml">
  <title>Body splash {nome} — 200 ml</title>
  <defs>
    <clipPath id="corpo-{slug}">
      <path d="M130 246 Q130 236 140 236 H260 Q270 236 270 246 V552 Q270 566 256 566 H144 Q130 566 130 552 Z"/>
    </clipPath>
  </defs>

  <!-- sobretampa transparente -->
  <rect x="139" y="42" width="122" height="176" rx="7" fill="#FFFFFF" opacity="0.3"/>
  <rect x="139" y="42" width="122" height="176" rx="7" fill="none" stroke="{VIDRO}" stroke-width="2.2"/>
  <line x1="151" y1="58" x2="151" y2="204" stroke="#FFFFFF" stroke-width="4" opacity="0.7"/>

  <!-- valvula -->
  <path d="M172 96 h56 a8 8 0 0 1 8 8 v34 h-72 v-34 a8 8 0 0 1 8 -8 z" fill="#FAFAFA" stroke="#D2D2D2" stroke-width="1.8"/>
  <rect x="186" y="80" width="28" height="18" rx="4" fill="#F2F2F2" stroke="#D2D2D2" stroke-width="1.6"/>
  <circle cx="200" cy="89" r="4.5" fill="#E4E4E4"/>

  <!-- gola dourada -->
  <rect x="158" y="140" width="84" height="50" rx="3" fill="{GOLD}"/>
{estrias}
  <rect x="158" y="140" width="84" height="50" rx="3" fill="none" stroke="{GOLD_ESCURO}" stroke-width="1.6"/>
  <rect x="163" y="145" width="7" height="40" rx="3" fill="#FFFFFF" opacity="0.5"/>

  <!-- gargalo -->
  <path d="M164 190 h72 l10 30 h-92 z" fill="#FFFFFF" opacity="0.5"/>
  <path d="M164 190 h72 l10 30 h-92 z" fill="none" stroke="{VIDRO}" stroke-width="2"/>
  <rect x="148" y="220" width="104" height="18" rx="4" fill="#FFFFFF" opacity="0.5" stroke="{VIDRO}" stroke-width="2"/>

  <!-- corpo -->
  <path d="M130 246 Q130 236 140 236 H260 Q270 236 270 246 V552 Q270 566 256 566 H144 Q130 566 130 552 Z" fill="#FFFFFF" opacity="0.62"/>

  <!-- respingo, recortado dentro do corpo -->
  <g clip-path="url(#corpo-{slug})">
{fitas}
{gotas}
  </g>

  <!-- contorno do corpo por cima do respingo -->
  <path d="M130 246 Q130 236 140 236 H260 Q270 236 270 246 V552 Q270 566 256 566 H144 Q130 566 130 552 Z" fill="none" stroke="{VIDRO}" stroke-width="2.4"/>
  <line x1="143" y1="262" x2="143" y2="452" stroke="#FFFFFF" stroke-width="5" opacity="0.55"/>
  <line x1="258" y1="262" x2="258" y2="392" stroke="#FFFFFF" stroke-width="2.5" opacity="0.4"/>
  <line x1="200" y1="242" x2="200" y2="296" stroke="{VIDRO}" stroke-width="2.6"/>

  <!-- rotulo -->
  <g text-anchor="middle" fill="{INK}">
    <text x="200" y="322" font-family="{SERIF}" font-size="25" letter-spacing="1.2">GOLDEN</text>
    <text x="200" y="346" font-family="{SERIF}" font-size="25" letter-spacing="1.2"><tspan fill="{GOLD}">&amp;</tspan>GRACE</text>
    <text x="200" y="386" font-family="{SANS}" font-size="9" letter-spacing="3.6">BODY SPLASH</text>
    <text x="200" y="418" font-family="{SERIF}" font-style="italic" font-size="24">{nome}</text>
    <text x="200" y="456" font-family="{SANS}" font-size="11" font-weight="700" letter-spacing="0.4">200ML | 6.76 FL.OZ</text>
    <text x="200" y="524" font-family="{SANS}" font-size="9" letter-spacing="1.4">DESODORANTE</text>
    <text x="200" y="536" font-family="{SANS}" font-size="9" letter-spacing="1.4">CORPORAL</text>
  </g>
</svg>
'''


def compactar(svg: str) -> str:
    """Tira comentários, recuo e quebras de linha — o arquivo vai para o 4G."""
    import re
    svg = re.sub(r"<!--.*?-->", "", svg, flags=re.S)
    svg = re.sub(r"\n\s*", "", svg)
    return re.sub(r">\s+<", "><", svg).strip() + "\n"


def main() -> None:
    DESTINO.mkdir(parents=True, exist_ok=True)
    for slug, nome, cor in FRAGRANCIAS:
        caminho = DESTINO / f"rotulo-{slug}.svg"
        caminho.write_text(compactar(montar(slug, nome, cor)), encoding="utf-8")
        print(f"{caminho.relative_to(RAIZ)}  {caminho.stat().st_size} bytes")


if __name__ == "__main__":
    main()
