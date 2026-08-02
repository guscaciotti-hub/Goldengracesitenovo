#!/usr/bin/env bash
# Baixa Playfair Display e Inter do Google Fonts e reduz cada arquivo ao que a
# página usa (ASCII + acentuação latina + pontuação), mantendo os eixos variáveis
# e as features de algarismo (lnum/tnum) referenciadas no CSS.
#
# Só precisa rodar de novo se você trocar as fontes ou usar caracteres novos.
# Requer: pip install fonttools brotli
set -euo pipefail
cd "$(dirname "$0")/.."

UNICODES="U+0020-007E,U+00A0-00FF,U+0152-0153,U+02BB-02BC,U+2013-2014,U+2018-201A,U+201C-201E,U+2026,U+2030,U+20AC,U+2122,U+2212"
FEATURES="kern,liga,clig,calt,lnum,tnum,pnum,onum,frac,ccmp,locl,mark,mkmk"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

baixar_e_reduzir() {
  local nome="$1" url="$2" peso_min="$3" peso_max="$4"
  curl -fsS "$url" -o "$TMP/$nome.woff2"
  pyftsubset "$TMP/$nome.woff2" \
    --output-file="$TMP/$nome.sub.woff2" \
    --flavor=woff2 --unicodes="$UNICODES" --layout-features="$FEATURES" \
    --no-hinting --desubroutinize
  # Corta o eixo variável na faixa de peso que o CSS realmente pede.
  # Se você usar um peso fora dela, ajuste aqui E no @font-face do index.html.
  python3 - "$TMP/$nome.sub.woff2" "assets/fonts/$nome.woff2" "$peso_min" "$peso_max" <<'PY'
import io, sys
from fontTools.ttLib import TTFont
from fontTools.varLib import instancer
origem, destino, minimo, maximo = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4])
f = instancer.instantiateVariableFont(TTFont(origem), {"wght": (minimo, maximo)}, updateFontNames=False)
buf = io.BytesIO(); f.flavor = "woff2"; f.save(buf)
open(destino, "wb").write(buf.getvalue())
PY
  printf '%-16s %6s -> %6s bytes\n' "$nome" \
    "$(stat -c%s "$TMP/$nome.woff2")" "$(stat -c%s "assets/fonts/$nome.woff2")"
}

mkdir -p assets/fonts
baixar_e_reduzir playfair-latin "https://fonts.gstatic.com/s/playfairdisplay/v40/nuFiD-vYSZviVYUb_rj3ij__anPXDTzYgA.woff2" 600 700
baixar_e_reduzir plex-latin     "https://fonts.gstatic.com/s/ibmplexsans/v23/zYXzKVElMYYaJe8bpLHnCwDKr932-G7dytD-Dmu1syxeKYY.woff2" 400 600
