# Landing page B2B — Golden &amp; Grace

Página única, estática, para venda do **Kit Vitrine** no atacado.
HTML + CSS inline, sem framework, sem build, sem backend. Só abrir `index.html`.

## Links

| | |
|---|---|
| **Site no ar** | <https://guscaciotti-hub.github.io/Goldengracesitenovo/> |
| Repositório | <https://github.com/guscaciotti-hub/Goldengracesitenovo> |
| Branch | [`claude/golden-grace-landing-page-6qrspf`](https://github.com/guscaciotti-hub/Goldengracesitenovo/tree/claude/golden-grace-landing-page-6qrspf) |
| Editar a página | [`index.html`](https://github.com/guscaciotti-hub/Goldengracesitenovo/edit/claude/golden-grace-landing-page-6qrspf/index.html) |
| Deploys | <https://github.com/guscaciotti-hub/Goldengracesitenovo/actions> |

Todo push na branch republica o site sozinho, em cerca de 30 segundos.

---

## 1. O que falta preencher

Enquanto sobrar qualquer token `PREENCHER_*`, uma faixa preta aparece no topo da
página listando o que falta — **ela some sozinha** quando o último for trocado.

Tudo em `index.html`. Busque e substitua:

| Token | O que é | Onde |
|---|---|---|
| `PREENCHER_DDDNUMERO` | Só os dígitos, com DDD: `13991234567` | 3 links de WhatsApp |
| `PREENCHER_PIXEL_ID` | ID do Pixel da Meta | `<head>` |
| `PREENCHER_DOMINIO` | Domínio final, sem `https://` | canonical + tags og |

**O rodapé é caso à parte.** Razão social, CNPJ, endereço, responsável e forma de
pagamento estão num bloco **comentado** no fim do `index.html`. Isso é
intencional: rodapé com "PREENCHER" à mostra destrói a confiança justamente do
lojista que a página quer convencer — melhor não mostrar do que mostrar vago.
Descomente o bloco e preencha antes de rodar tráfego.

O link do WhatsApp já vai com mensagem pronta — a conversa começa com o lojista
dizendo o que quer, e você não perde tempo perguntando:

```
https://wa.me/55DDDNUMERO?text=Tenho%20loja%20na%20Baixada%20e%20quero%20o%20Kit%20Vitrine
```

---

## 2. As fotos dos produtos

Os arquivos `assets/rotulo-*.svg` são **desenhos vetoriais de apoio**, na
identidade da marca, para a página não ficar vazia até as fotos entrarem.
**Troque pelas fotos reais antes de rodar tráfego.**

1. Exporte cada foto em **WebP, no máximo 800px de largura**, fundo claro.
2. Salve em `assets/` com estes nomes exatos:
   `rotulo-sweet-reign.webp`, `rotulo-royal-bloom.webp`, `rotulo-midnight-grace.webp`,
   `rotulo-azure-mist.webp`, `rotulo-golden-aura.webp`
3. Em `index.html`, troque `.svg` por `.webp` nas 5 tags `<img>`.
4. Ajuste `width` e `height` de cada `<img>` para as dimensões reais, para o
   layout não pular enquanto a foto carrega.

Converter: `cwebp -q 82 -resize 800 0 foto.jpg -o assets/rotulo-sweet-reign.webp`

---

## 3. Rastreamento

A página tem **um CTA só**, então tem um evento só que importa.

| Ação | Evento |
|---|---|
| Abertura da página | `PageView` |
| Clique em "Falar no WhatsApp" (hero, fechamento e botão flutuante) | `Contact` |

O Pixel só carrega depois que `PREENCHER_PIXEL_ID` for trocado — até lá a página
não faz nenhuma requisição para a Meta. Para marcar um evento novo em qualquer
link, basta pôr `data-evento="NomeDoEvento"` na tag.

---

## 4. Publicar

Já está no **GitHub Pages**, servindo a raiz da branch.
`.github/workflows/pages.yml` republica a cada push, em ~30 s.

Domínio próprio: *Settings → Pages → Custom domain*. Depois troque
`PREENCHER_DOMINIO` no `index.html`.

`vercel.json` e `netlify.toml` ficam no repositório caso um dia mude de
hospedagem — o Pages ignora os dois.

---

## 5. Scripts

Nada disso é necessário para a página funcionar. Só para regerar arquivos.

| Comando | O que faz |
|---|---|
| `python3 tools/gerar-frascos.py` | Regera os SVGs de apoio dos frascos |
| `python3 tools/gerar-og.py` | Regera `assets/og.png`, a imagem de compartilhamento |
| `./tools/preparar-fontes.sh` | Baixa e reduz as fontes |
| `python3 tools/testar.py` | Sobe a página e tira prints em 375px e 1280px |
| `python3 tools/gerar-preview.py` | Versão de arquivo único, tudo embutido |

Dependências: `pip install fonttools brotli pillow playwright`

---

## 6. Decisões de design

**O conceito é tabela de preços de atacado**, não landing page. Tudo alinhado à
esquerda, micro-rótulos em caixa alta, fios capilares, algarismos tabulares — o
formato que esse lojista reconhece como "gente que faz isso todo dia". Nada é
centralizado, porque hero centralizado é a assinatura de LP genérica.

**O dourado aparece em exatamente 3 lugares:** o "&" do logo, o bloco da margem
(o R$ 470 e o respingo que serve de chão dele) e o fio ao lado de "Você não paga
nada agora". O "R$ 329" do hero é **preto de propósito** — assim o único número
dourado da página inteira é o lucro do lojista.

**Dois tons do mesmo dourado.** `#C89B5F` é o da marca, usado sobre preto.
Sobre branco ele dá 2,5:1 e reprova em acessibilidade, então texto dourado em
fundo claro usa `#8C6224` — mesma cor, tom fechado, 5,4:1. É por isso que o
bloco da margem é uma chapa preta: é onde o dourado da marca aparece cheio,
com 6,2:1 mesmo por cima do respingo.

**Tipografia:** Playfair Display no display (o didone que corresponde ao logo) e
**IBM Plex Sans** no corpo — registro de documento comercial, não a neutralidade
de SaaS. Self-hosted e reduzidas: 58 KB nas duas, sem CDN externo, o que
economiza dois handshakes no 4G.

**Algarismos alinhados forçados** no Playfair, que vem com os antigos por padrão
— o 3 e o 9 desciam da linha de base e atrasavam a leitura do preço.

**O botão do WhatsApp tem texto preto**, não branco: branco sobre `#25D366` dá
2:1 e some no sol do balcão. Preto dá 9,5:1.

**A garantia de troca saiu do hero.** Ela tem seção própria e volta no CTA
final; ao lado do botão, competia com "você não paga nada agora", que é o
argumento mais forte da oferta. O hero ficou com preço, promessa de pagamento
e botão — nada mais.
