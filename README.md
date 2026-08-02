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
| Deploys | <https://github.com/guscaciotti-hub/Goldengracesitenovo/actions> |

Todo push republica o site sozinho, em ~30 s.

---

## 1. Como as fotos entram

**Você não precisa mexer no código.** Cada bloco que depende de foto fica
escondido até o arquivo existir no repositório. Assim que a foto entra, o bloco
aparece sozinho. Moldura vazia numa página cujo trabalho é provar que a empresa
existe faz exatamente o efeito contrário.

| Arquivo | O que acende |
|---|---|
| `assets/logo.png` | logo oficial no lugar do logotipo tipográfico |
| `assets/hero-composicao.webp` | segunda coluna do hero; o layout vira 55/45 |
| `assets/frascos/{sweet-reign,royal-bloom,midnight-grace,azure-mist,golden-aura}.webp` | foto em cada card de fragrância |
| `assets/prova/avaliacao-01..04.webp` | bloco de avaliações |
| `assets/prova/loja-01..03.webp` | bloco "já está no balcão" |
| `assets/socios.webp` + `assets/estoque.webp` | seção "A gente entrega pessoalmente" |

WebP, máximo 1000px de largura. Pode subir `.jpg` que a conversão é um comando:
`cwebp -q 82 -resize 1000 0 foto.jpg -o assets/frascos/sweet-reign.webp`

Nas fotos de loja, troque `PREENCHER_LOJA_1..3` no `index.html` pelo nome do
estabelecimento. Enquanto não trocar, a legenda simplesmente não aparece — foto
com token à mostra é pior que foto sem legenda.

---

## 2. O que falta preencher

| Token | O que é |
|---|---|
| `PREENCHER_DDDNUMERO` | só os dígitos com DDD, ex. `13991234567` — **3 botões** |
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

## 4. Estrutura

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

## 5. Decisões de design

**Zero imagem gerada.** Não há textura, respingo desenhado nem frasco vetorial
na página. Numa página que existe para provar que a empresa é real, imagem
gerada trabalha contra — e um lojista que já foi abordado por dezenas de
fornecedores reconhece isso na hora. Enquanto não houver foto de verdade, o peso
visual vem de tipografia. Foi por isso que os `rotulo-*.svg` das versões
anteriores saíram.

**O conceito é tabela de preços de atacado**, não landing page: tudo alinhado à
esquerda no mesmo eixo, micro-rótulos em caixa alta, fios capilares, algarismos
tabulares.

**O dourado aparece em 2 lugares:** o "&" do logo e o R$ 470. O "R$ 329" do hero
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

---

## 6. Scripts

| Comando | O que faz |
|---|---|
| `python3 tools/gerar-og.py` | regera `assets/og.png`, a imagem de compartilhamento |
| `./tools/preparar-fontes.sh` | baixa e reduz as fontes |
| `python3 tools/testar.py` | sobe a página e tira prints em 375px e 1440px |
| `python3 tools/gerar-preview.py` | versão de arquivo único, tudo embutido |

Dependências: `pip install fonttools brotli pillow playwright`
