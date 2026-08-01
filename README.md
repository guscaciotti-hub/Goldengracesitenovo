# Landing page B2B — Golden &amp; Grace

Página única, estática, para venda do **Kit Vitrine** no atacado.
HTML + CSS inline, sem framework, sem build, sem backend. Só abrir `index.html`.

---

## 1. O que falta preencher

A página está pronta, mas os dados reais ainda não existem. Enquanto qualquer
token `PREENCHER_*` estiver no arquivo, um aviso preto aparece no topo da página
listando o que falta — **ele some sozinho** quando tudo for substituído.

Tudo está em `index.html`. Busque e substitua:

| Token | O que é | Onde aparece |
|---|---|---|
| `PREENCHER_LINK_COMPRAR` | Link de pagamento (Mercado Pago / InfinitePay) | 2 botões "Comprar agora" |
| `PREENCHER_LINK_WHATSAPP` | `https://wa.me/55DDDNUMERO?text=Oi,%20quero%20o%20Kit%20Vitrine` | 2 botões + botão flutuante |
| `PREENCHER_PIXEL_ID` | ID do Pixel da Meta | `<head>` |
| `PREENCHER_DOMINIO` | Domínio final, sem `https://` | canonical + tags og |
| `PREENCHER_RAZAO_SOCIAL` | Razão social | rodapé |
| `PREENCHER_CNPJ` | CNPJ | rodapé |
| `PREENCHER_ENDERECO` | Endereço em São Vicente | rodapé |
| `PREENCHER_RESPONSAVEL` | Seu nome | rodapé |
| `PREENCHER_PARCELAMENTO` | ex.: `em até 3x no cartão` ou `no Pix ou cartão` | rodapé |

Num editor de código, "Substituir em todos os arquivos" resolve cada um de uma vez.

> O link do WhatsApp já vai com `?text=` pré-preenchido — assim a conversa começa
> com o lojista dizendo o que quer, e você não perde tempo perguntando.

---

## 2. As fotos dos produtos

Os arquivos `assets/rotulo-*.svg` são **desenhos vetoriais de apoio**, na
identidade da marca, feitos para a página não ficar vazia até as fotos entrarem.
**Troque pelas fotos reais antes de rodar tráfego.**

Como trocar:

1. Exporte cada foto em **WebP, no máximo 800px de largura**, fundo claro.
2. Salve em `assets/` com estes nomes exatos:
   `rotulo-sweet-reign.webp`, `rotulo-royal-bloom.webp`, `rotulo-midnight-grace.webp`,
   `rotulo-azure-mist.webp`, `rotulo-golden-aura.webp`
3. Em `index.html`, troque `.svg` por `.webp` nas 5 tags `<img>` da seção de fragrâncias.
4. Ajuste `width` e `height` de cada `<img>` para as dimensões reais do arquivo
   (isso evita o layout "pular" enquanto a foto carrega).

Para converter: `cwebp -q 82 -resize 800 0 foto.jpg -o assets/rotulo-sweet-reign.webp`

O mesmo vale para `assets/og.png` (a imagem que aparece quando o link é
compartilhado no WhatsApp) — dá para regerar com `python3 tools/gerar-og.py`.

---

## 3. Rastreamento

O Pixel só carrega depois que `PREENCHER_PIXEL_ID` for substituído — até lá a
página não faz nenhuma requisição para a Meta.

| Ação | Evento disparado |
|---|---|
| Clique em "Comprar agora" (topo e fechamento) | `InitiateCheckout` |
| Clique em "Falar no WhatsApp" (topo, fechamento e botão flutuante) | `Contact` |
| Abertura da página | `PageView` |

É isso que responde, depois de ~3 semanas, qual das duas rotas traz pedido —
e qual dá para matar.

Para marcar um evento novo em qualquer link, basta adicionar
`data-evento="NomeDoEvento"` na tag.

---

## 4. Publicar

O repositório já traz `vercel.json` e `netlify.toml` (cache longo nas fontes,
cache curto nas imagens, para as fotos novas aparecerem sem esperar).

**Vercel:** importe o repositório. Sem framework, sem build command, output
directory `.`.

**Netlify:** arraste a pasta em <https://app.netlify.com/drop>, ou conecte o
repositório — o `netlify.toml` já configura tudo.

---

## 5. Scripts auxiliares

Nada disso é necessário para a página funcionar. Só para regerar arquivos.

| Comando | O que faz |
|---|---|
| `python3 tools/gerar-frascos.py` | Regera os SVGs de apoio dos frascos |
| `python3 tools/gerar-og.py` | Regera `assets/og.png` |
| `./tools/preparar-fontes.sh` | Baixa e reduz as fontes (só se trocar de fonte) |
| `python3 tools/testar.py` | Sobe a página e tira prints em 375px e 1280px |

Dependências dos scripts: `pip install fonttools brotli pillow playwright`

---

## 6. Decisões que valem saber

- **Fontes self-hosted e reduzidas** (Playfair Display + Inter, 73 KB no total).
  Sem Google Fonts CDN: economiza dois handshakes no 4G.
- **Dois tons de dourado.** `#C89B5F` é o dourado da marca, usado sobre preto e
  em fios. Sobre branco ele tem contraste 2,5:1 e reprova em acessibilidade, então
  texto dourado em fundo claro usa `#8C6224` — mesma cor, tom fechado, 5,4:1.
- **O bloco preto do "R$ 470"** existe por isso: é onde o dourado da marca aparece
  no seu tom cheio, com 7,5:1 de contraste. E é o momento visual da página.
- **O botão do WhatsApp tem texto preto**, não branco: branco sobre `#25D366` dá
  2:1 e é ilegível no sol. Preto dá 9,5:1.
- **Sem contador regressivo, sem "últimas unidades".** Lojista já viu isso mil vezes.
