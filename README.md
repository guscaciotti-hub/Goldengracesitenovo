# Landing page B2B — Golden &amp; Grace

Página única, estática, para venda do **Kit Vitrine** no atacado.
HTML + CSS inline, sem framework, sem build, sem backend.

## Links

| | |
|---|---|
| **Site no ar** | <https://guscaciotti-hub.github.io/Goldengracesitenovo/> |
| Repositório | <https://github.com/guscaciotti-hub/Goldengracesitenovo> |
| Editar a página | [`index.html`](https://github.com/guscaciotti-hub/Goldengracesitenovo/edit/claude/golden-grace-landing-page-6qrspf/index.html) |
| Subir fotos | [`assets/`](https://github.com/guscaciotti-hub/Goldengracesitenovo/upload/claude/golden-grace-landing-page-6qrspf/assets) |
| Página de pedido | <https://guscaciotti-hub.github.io/Goldengracesitenovo/pedido.html> |
| Deploys | <https://github.com/guscaciotti-hub/Goldengracesitenovo/actions> |

Todo push republica o site sozinho, em ~30 s.

---

## 1. As fotos

As fotos oficiais e o logo já estão na página. Os originais ficam em
`assets/originais/`; `python3 tools/preparar-imagens.py` gera o que a página
usa. **Só rode de novo se trocar os originais.**

O que o processamento faz: as cinco fotos vieram do mesmo rig — fundo `#ECEAEB`
liso e o frasco no mesmo lugar em todas — então dá para recortar o fundo por
inundação a partir das bordas (chave de cor global comeria o vidro claro),
recortar as cinco no mesmo enquadramento e montar o lineup do hero sobrepondo
os frascos de verdade.

**Os blocos que ainda não têm foto continuam escondidos** até o arquivo existir.
Moldura vazia numa página cujo trabalho é provar que a empresa existe faz
exatamente o efeito contrário.

Ainda faltam:

| Arquivo | O que acende |
|---|---|
| `assets/prova/avaliacao-01..04.webp` | bloco de avaliações |
| `assets/prova/loja-01..03.webp` | bloco "já está no balcão" |
| `assets/socios.webp` + `assets/estoque.webp` | seção "A gente entrega pessoalmente" |

Pode subir `.jpg` — eu converto para WebP no processamento.

Nas fotos de loja, troque `PREENCHER_LOJA_1..3` no `index.html` pelo nome do
estabelecimento. Enquanto não trocar, a legenda simplesmente não aparece — foto
com token à mostra é pior que foto sem legenda.

---

## 2. O que falta preencher

| Token | O que é |
|---|---|
| `PREENCHER_DDDNUMERO` | só os dígitos com DDD, ex. `13991234567` — **3 botões** |
| `PREENCHER_ENDPOINT_EVOLUZECHAT` | endpoint do webhook — em `pedido.html` |
| `PREENCHER_TOKEN` | token do webhook — em `pedido.html` |
| `PREENCHER_PIXEL_ID` | ID do Pixel da Meta |
| `PREENCHER_DOMINIO` | domínio final, sem `https://` |
| `PREENCHER_LOJA_1..3` | nome das lojas nas fotos de balcão |

**Dois blocos comentados no `index.html` precisam ser abertos:**

- **O rodapé legal** — razão social, CNPJ, endereço, responsável e forma de
  pagamento. É o principal elemento de credibilidade da página. Está comentado
  porque rodapé com "PREENCHER" à mostra prova o contrário do que a página
  inteira tenta provar.
- **A pergunta "Preciso ter CNPJ?"** — falta a resposta. É provavelmente a
  primeira dúvida do lojista.

Em "A gente entrega pessoalmente", há um comentário indicando onde entram os
nomes dos sócios.

---

## 3. Rastreamento

Um CTA só, um evento que importa.

| Ação | Evento |
|---|---|
| Abertura | `PageView` |
| Clique em "Falar no WhatsApp" (hero, fechamento, flutuante) | `Contact` |

O Pixel só carrega depois que o ID for preenchido. Para marcar um evento novo,
basta pôr `data-evento="Nome"` na tag.

---

## 4. Página de pedido

`pedido.html` é separada da landing e **não é o caminho principal**: quem chega
pela campanha cai no WhatsApp, e é o agente que manda este link depois de
qualificar o lojista. A landing só tem um atalho em texto no fechamento, sem
peso de botão, para quem já sabe o que quer.

A oferta é Kit Vitrine, 5 unidades entre as 5 fragrâncias, R$ 169, pagamento na
entrega. O lojista escolhe **quantos kits** levar (teto de 10) e distribui as
unidades entre as fragrâncias; o preço acompanha, `169 × kits`.

O `+` de cada fragrância nunca fica desabilitado. Travar o botão quando o total
fecha faz a tela parecer que só dá para pedir uma de cada — passar do total é
permitido e avisado em vermelho, e o envio é que bloqueia.

O contrato do webhook, os pontos da spec que precisam de ajuste e o que fazer
quando o POST falha estão em **[INTEGRACAO-EVOLUZECHAT.md](INTEGRACAO-EVOLUZECHAT.md)**.

---

## 5. Domínio próprio

O site atende em **atacado.goldengrace.com.br**.

**Por que subdomínio e não o domínio raiz.** `goldengrace.com.br` já responde
pelo Shopify (`23.227.38.65`) — é a loja de varejo, a mesma para onde o agente
manda consumidora final. Apontar o raiz para o GitHub Pages derrubaria essa
loja. Com subdomínio, nada do que já existe é tocado.

**Passo 1 — no painel do registro.br**, na zona DNS, um registro só:

| Tipo | Nome | Valor |
|---|---|---|
| CNAME | `atacado` | `guscaciotti-hub.github.io.` |

O ponto final no fim não é erro de digitação. **Não mexa em nenhum registro
existente** — os do Shopify continuam como estão.

**Passo 2 — Settings → Pages → Custom domain**: escreva
`atacado.goldengrace.com.br` e salve. Quando o DNS propagar, marque
**Enforce HTTPS**; o certificado é automático e leva alguns minutos.

Propagação no `.br` costuma levar de minutos a algumas horas. Até lá o
`github.io` segue no ar, e depois passa a redirecionar para o domínio novo.

**Editar continua igual:** push na branch, republica em ~30 s.

Para trocar de endereço depois (outro subdomínio, ou o raiz caso a loja saia
do Shopify): `./tools/aplicar-dominio.sh novo.endereco.com.br`.

---

## 6. Estrutura

```
1. Hero               8. Entrega
2. Margem             9. Perguntas diretas
3. Por que a gente   10. CTA final
4. As 5 fragrâncias  11. Rodapé
5. Prova         ← só com foto
6. Quem somos    ← só com foto
7. Garantia
```

---

## 7. Decisões de design

**Zero imagem gerada.** Não há textura, respingo desenhado nem frasco vetorial.
Tudo que aparece é foto real ou tipografia. Numa página que existe para provar
que a empresa é real, imagem gerada trabalha contra — um lojista que já foi
abordado por dezenas de fornecedores reconhece isso na hora.

**O véu de cor em cada card de fragrância não é enfeite.** O frasco é de vidro
transparente e, recortado do fundo, sobre branco ele some. Cada tile recebe um
véu de 14% da cor do respingo do próprio rótulo: dá contorno ao vidro e é o que
diferencia um card do outro.

**O conceito é tabela de preços de atacado**, não landing page: tudo alinhado à
esquerda no mesmo eixo, micro-rótulos em caixa alta, fios capilares, algarismos
tabulares.

**O dourado aparece em 2 lugares:** o "&" do logo e o R$ 230. O "R$ 169" do hero
é preto de propósito — assim o único número dourado da página é o lucro do
lojista. Sobre branco o `#C89B5F` dá 2,5:1 e reprova em acessibilidade; é por
isso que o bloco da margem é uma chapa preta, onde ele chega a 7,5:1.

**Botão preto com ícone verde.** Bloco cheio de `#25D366` briga com a paleta.
Largura automática no desktop, total no mobile. O flutuante só aparece depois
que o hero sai da tela — com o botão principal à vista, dois CTAs competiriam
pela mesma decisão.

**Hero em dois estados.** Sem a foto dos frascos, a coluna da direita carrega a
oferta (promessa, botão e troca) para a página não abrir com metade da tela
vazia. Com a foto, a oferta desce e a imagem assume a direita, no 55/45.

**Tipografia:** Playfair Display no display, IBM Plex Sans no corpo — registro de
documento comercial, não a neutralidade de SaaS. Self-hosted e reduzidas: 58 KB
nas duas, sem CDN externo.

**A lista de cidades saiu da seção de entrega.** Repetia, palavra por palavra, a
frase da linha de cima.

**O lucro é R$ 230, não R$ 230,50.** A margem por unidade é R$ 46,10 e 5 × 46,10
dá R$ 230,50. A página mostra R$ 230 — arredondar para baixo nunca promete
demais — e a nota diz "margem de R$ 46,10 por unidade" em vez de mostrar a
multiplicação, que apareceria errada na tela.

---

## 8. Scripts

| Comando | O que faz |
|---|---|
| `./tools/aplicar-dominio.sh dominio.com.br` | liga o domínio próprio: cria o CNAME e preenche as tags |
| `python3 tools/preparar-imagens.py` | recorta o fundo das fotos, gera os cards e o lineup do hero |
| `python3 tools/gerar-og.py` | regera `assets/og.png`, o cartão de compartilhamento |
| `./tools/preparar-fontes.sh` | baixa e reduz as fontes |
| `python3 tools/testar.py` | sobe a página e tira prints em 375px e 1440px |
| `python3 tools/gerar-preview.py` | versão de arquivo único, tudo embutido |

Dependências: `pip install fonttools brotli pillow playwright`
