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
  local nome="$1" url="$2"
  curl -fsS "$url" -o "$TMP/$nome.woff2"
  pyftsubset "$TMP/$nome.woff2" \
    --output-file="assets/fonts/$nome.woff2" \
    --flavor=woff2 --unicodes="$UNICODES" --layout-features="$FEATURES" \
    --no-hinting --desubroutinize
  printf '%-16s %6s -> %6s bytes\n' "$nome" \
    "$(stat -c%s "$TMP/$nome.woff2")" "$(stat -c%s "assets/fonts/$nome.woff2")"
}

mkdir -p assets/fonts
baixar_e_reduzir playfair-latin "https://fonts.gstatic.com/s/playfairdisplay/v40/nuFiD-vYSZviVYUb_rj3ij__anPXDTzYgA.woff2"
baixar_e_reduzir inter-latin     "https://fonts.gstatic.com/s/inter/v20/UcC73FwrK3iLTeHuS_nVMrMxCp50SjIa1ZL7.woff2"
