#!/usr/bin/env bash
# Liga o domínio próprio ao site. Uso:  ./tools/aplicar-dominio.sh loja.exemplo.com.br
#
# Faz duas coisas:
#   1. cria o arquivo CNAME, que é o que mantém o domínio preso ao deploy
#   2. troca PREENCHER_DOMINIO pelas tags canonical e og das duas páginas
#
# O github.io continua funcionando: passa a redirecionar para o domínio novo.
set -euo pipefail
cd "$(dirname "$0")/.."

DOM="${1:-}"
[ -z "$DOM" ] && { echo "uso: $0 seudominio.com.br"; exit 1; }
case "$DOM" in *//*|*/*) echo "erro: informe só o domínio, sem https:// e sem barra"; exit 1;; esac

# O CNAME precisa ir junto no artefato publicado. Sem ele, um deploy seguinte
# pode derrubar o domínio configurado em Settings.
printf '%s\n' "$DOM" > CNAME
sed -i "s/PREENCHER_DOMINIO/$DOM/g" index.html pedido.html

echo "CNAME criado com $DOM"
echo "ocorrências restantes de PREENCHER_DOMINIO: $(grep -c PREENCHER_DOMINIO index.html pedido.html | paste -sd+ | bc)"
echo
echo "Falta, no painel do registro.br, apontar o DNS — os registros estão no README."
