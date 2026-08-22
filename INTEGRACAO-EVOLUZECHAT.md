# Integração EvoluzeChat — contrato do lado da página

Este documento cobre **só o que a página faz**. Os itens 2 a 8 da especificação
(grupo de WhatsApp, agendamentos, comandos, painel) rodam dentro do EvoluzeChat
e dependem das respostas de viabilidade que só o fornecedor pode dar.

## As 3 perguntas de viabilidade

**Não tenho como responder.** Não tenho acesso ao EvoluzeChat nem à documentação
dele. Webhook de entrada, envio para grupo e agendamento futuro são capacidades
do produto — quem responde é o fornecedor. O que dá para adiantar:

- Se **não** houver webhook de entrada (pergunta 1), a Fase 1 inteira cai. A
  página precisa de um endpoint para onde postar.
- Se **não** houver envio para grupo (pergunta 2), a própria spec já resolve:
  disparo individual para os dois números. Não trava nada.
- Se **não** houver agendamento (pergunta 3), D+7/D+20/D+45 precisam de um
  agendador externo chamando o EvoluzeChat. Isso é backend, e a página estática
  não resolve.

---

## O que a página envia

`pedido.html` faz `POST` com `Content-Type: application/json` e
`Authorization: Bearer <token>`, no formato exato do item 1:

```json
{
  "evento": "pedido_confirmado",
  "id": "GG-1787361264-JIVM3P",
  "criado_em": "2026-08-22T14:32:00-03:00",
  "kit": "Kit Vitrine 5 un",
  "valor": 169,
  "fragrancias": {"sweet_reign":1,"royal_bloom":1,"midnight_grace":1,"azure_mist":1,"golden_aura":1},
  "total_unidades": 5,
  "loja": "Perfumaria Aurora",
  "responsavel": "Marina",
  "whatsapp": "13998124455",
  "cidade": "São Vicente",
  "bairro": "Itararé",
  "endereco": "Rua Frei Gaspar, 812, loja 3",
  "referencia": "em frente à praça",
  "data_entrega": "2026-08-23",
  "janela": "Manhã",
  "pagamento": "Pix",
  "utm_source": "meta", "utm_medium": "cpc", "utm_campaign": "vitrine5",
  "mensagem_grupo": "...",
  "origem": "landing_pedido"
}
```

`valor` e `total_unidades` são números. `whatsapp` vai só com dígitos.
`fragrancias` sempre traz as 5 chaves, inclusive as zeradas.

**`valor` não é fixo.** O lojista pode levar mais de um kit, então
`valor = 169 × kits` e `total_unidades = 5 × kits` (teto de 10 kits na página).
Com mais de um kit, `kit` vem como `"Kit Vitrine 5 un x3"` e a mensagem do grupo
diz `15 un (3 kits) — R$ 507`. **Não cravem 169 nem 5 do lado de vocês** — leiam
sempre `valor` e `total_unidades` do payload.

`mensagem_grupo` já vem pronta, no formato do item 2 — é só repassar:

```
NOVO PEDIDO — GG-1787361264-JIVM3P
Perfumaria Aurora · Itararé, São Vicente
5 un — R$ 169 — Pix na entrega
domingo, 23/08 — Manhã
Rua Frei Gaspar, 812, loja 3
Ref: em frente à praça
Contato: 13998124455
Sweet Reign 1 · Royal Bloom 1 · Midnight Grace 1 · Azure Mist 1 · Golden Aura 1
```

A linha `Ref:` some quando não há referência. O `id` já contém o prefixo `GG-`,
então na mensagem ele aparece uma vez só, não `GG-GG-...`.

---

## Três coisas da spec que precisam de ajuste

**1. O `id` da spec pode perder pedido.** `GG-1740000000` é epoch em segundos e a
regra é ignorar `id` repetido. Dois pedidos no mesmo segundo → o segundo é
descartado como duplicata. É o "nenhum pedido pode se perder silenciosamente"
falhando exatamente onde ninguém olha. A página gera
`GG-<epoch>-<6 caracteres aleatórios>`. **Mantenham a dedup por `id` completo**,
não por prefixo de tempo.

**2. O token é público.** A página é estática: o token está no código-fonte e
qualquer um lê. Ele identifica a origem, não autentica o lojista. O endpoint
precisa tratá-lo como segredo público — limitar taxa por IP, recusar payload
fora do formato, e nunca disparar nada irreversível só com base nele.

**3. O endpoint precisa liberar CORS** para o domínio da página, incluindo
resposta ao `OPTIONS` de preflight (por causa do header `Authorization`).
Sem isso o navegador bloqueia antes de sair a requisição.

---

## Se o POST falhar

A página não deixa o pedido sumir:

1. O pedido é gravado em `localStorage` **antes** da primeira tentativa. Se a aba
   morrer no meio, ele sobrevive.
2. Retentativa em 0s, 2s, 8s e 20s enquanto a página está aberta.
3. O que sobrar na fila é reenviado na próxima visita.
4. Se mesmo assim não passar, a tela de confirmação troca de discurso e oferece
   **enviar o pedido pelo WhatsApp**, com a mensagem já montada. O lojista toca
   uma vez e o pedido chega na equipe.

Como a página é estática, o item 4 é a única garantia real de que um pedido não
se perde quando o endpoint está fora do ar. É a rota de socorro, não o caminho.

---

## Antes de publicar

No topo do `<script>` de `pedido.html`:

```js
var CONFIG = {
  endpoint: 'https://PREENCHER_ENDPOINT_EVOLUZECHAT',
  token:    'PREENCHER_TOKEN',
  whatsapp: '55PREENCHER_DDDNUMERO'
};
```

Enquanto o endpoint não existir, todo pedido cai na rota de socorro do WhatsApp —
a página funciona, mas sem registro automático.

---

## O que a página não faz

Bairros atendidos (item 7) não são validados aqui: a página só pergunta cidade
entre as quatro atendidas. A checagem de bairro está no agente, que qualifica
**antes** de mandar este link — que é o comportamento certo, porque não dá para
coletar o pedido inteiro e cancelar depois.
