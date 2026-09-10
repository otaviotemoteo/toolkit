# toolkit: contrato de trabalho

Leia inteiro antes de agir. Se algo aqui contradisser outro arquivo, este vale.

---

## O que é este repo

A ferramenta que gera os assets visuais do portfólio do Otávio, e que sobrevive
ao portfólio: é com ela que ele vai gerar imagem para os próximos projetos.

Ele é um dos quatro entregáveis. Os outros são `portfolio` (os assets e o site),
`skills` (as skills e playbooks extraídos) e `otaviotemoteo` (o README do
perfil). **Não misture os quatro.** Este repo produz imagem, e mais nada.

## A restrição que decide tudo

**O Otávio não faz trabalho manual de designer.** Nada de Figma, Illustrator,
vetorizador ou limpeza de path à mão. Se uma solução exigir desenho manual, ela
é a solução errada: pare e proponha outra.

## Antes de gerar qualquer coisa

**Nada é gerado sem briefing aprovado.** Vale para toda imagem, animação e
vídeo. O fluxo é: escrever o briefing → o Otávio aprova ou corrige → só então
gerar. Se o resultado sair errado, **revise o briefing antes de gerar de novo**.
Regerar com o mesmo briefing esperando resultado diferente é como se queima
crédito.

Cada briefing mora em `briefs/<nome>/brief.md`. O de `hero-character` é o
modelo: tem `## Prompt`, que é o que a CLI extrai, e `## Acceptance`, que é
como saber que ficou certo.

**Critério de aceite tem que ser observável.** "Nenhuma área preenchida de preto
maior que o cabelo" serve. "Ficou bonito" não.

## Custo

**Sempre avise o custo estimado antes de gastar crédito, e espere confirmação
para vídeo.**

| Conta | Para quê | Estado |
|---|---|---|
| `platform.openai.com` | imagem, fase 1 | key criada e válida. **Sem crédito**: a API responde 429 `insufficient_quota` (testado 2026-09-04). Os $5 de conta nova não existem mais, ou não valem para esta conta. |
| `aistudio.google.com` | texto | key sem cartão, tier gratuito funciona **para texto**. Imagem tem `limit: 0` em todos os seis modelos (testado 2026-09-04). |
| local, `mflux` | **imagem, fase 1** | rota atual. Sem conta, sem cota, sem custo. |
| `zenmux.ai` | vídeo, fase 2 | só depois da spec aprovada |

**Não há cartão.** Isso não é um detalhe de conta, é a restrição que decide a
rota da fase 1. Duas afirmações de crédito gratuito foram testadas e as duas
eram falsas: os $5 de conta nova na OpenAI e o tier gratuito de imagem do
Gemini. Trate qualquer terceira como hipótese até uma chamada real dizer o
contrário. Render em tier pago continua sendo decisão que alguém digita.

## Como usar

```bash
python3.11 -m venv .venv && ./.venv/bin/pip install -r requirements.txt

# monta o prompt e mostra, sem gerar e sem custo
./.venv/bin/python src/generate.py briefs/hero-character/brief.md --dry-run

# gera um placeholder, exercita o pipeline inteiro sem key
./.venv/bin/python src/generate.py briefs/hero-character/brief.md

# gera de verdade, local, sem custo
make setup-local   # uma vez
IMAGE_BACKEND=local ./.venv/bin/python src/generate.py briefs/hero-character/brief.md

# recorta o fundo chroma
./.venv/bin/python ~/.claude/skills/oil-visual/scripts/cutout.py origem.png transparente.png
```

O resultado cai em `briefs/<nome>/out/`, com nome versionado e um `.json` ao
lado guardando o prompt exato. **Nunca sobrescreva um asset aprovado.**

## Verificação

Um comando responde se o repo está em estado de continuar. Roda em menos de meio
segundo, sem key e sem custo.

```bash
make check      # tudo abaixo, nesta ordem
make lint       # ruff em src/ e scripts/
make briefs     # todo diretório de asset tem o seu brief.md
make anchors    # os blocos positivo e negativo não se contradizem
make solutions  # toda lição registrada aponta para algo que existe
make mutation   # prova que cada check consegue reprovar
make smoke      # o pipeline inteiro roda ponta a ponta no backend fake
make setup      # recria o venv
make setup-local  # instala a pilha de geração local (pesada)
```

`make mutation` roda cada check contra os fixtures quebrados de propósito em
`tests/fixtures/`. Se um deles passar, o quebrado é o check, não o fixture. Todo
fixture ali é um erro que aconteceu de verdade, não um inventado.

## Aprendizado

Toda lição que custou alguma coisa vira um arquivo em `docs/solutions/`, um por
lição, com frontmatter dizendo **o que a garante**: um check, uma regra da spec,
ou prosa. Nessa ordem de preferência. Lição que fica em prosa podendo ser check
é lição que vai ser aprendida de novo.

`make solutions` falha se alguma delas apontar para um check ou fixture que não
existe mais. É assim que se percebe harness apodrecendo, porque ele não quebra,
só vai valendo menos em silêncio.

Antes de acrescentar regra aqui, pergunte se ela não pertence a um documento
temático. Este arquivo só cresce quando a restrição é inegociável.

## Estado entre sessões

**Leia `PROGRESS.md` no início de toda sessão e atualize antes de encerrar.** O
que foi decidido na conversa e não está lá não aconteceu.

## Arquitetura

```
docs/ILLUSTRATION_SPEC.md   o sistema visual. Uma cópia do style anchor, só.
src/adapters/base.py        a interface. Nada acima dela sabe qual vendor rodou.
src/adapters/fake.py        placeholder, sem key, sem custo
src/adapters/openai_backend.py
src/adapters/zenmux.py      não testado; existe para provar que a interface é interface
src/adapters/__init__.py    registro, escolha por IMAGE_BACKEND
src/generate.py             briefing + anchor da spec + backend
briefs/<nome>/brief.md      um por asset
briefs/<nome>/out/          resultados versionados, com o prompt ao lado
```

**Por que o adaptador existe:** para não ficar preso a provider. A dependência é
de build, não de runtime: os assets são arquivos estáticos e o site pronto não
chama API nenhuma. Trocar de vendor é um arquivo novo em `adapters/` mais uma
variável de ambiente. A spec de prompt é do Otávio e não muda.

**O style anchor mora só na spec.** `generate.py` extrai por regex. Mudar o
sistema visual é uma edição, não uma busca por todos os briefings já escritos.

## O sistema visual, em uma linha

**O estático é tinta sobre papel. A cor vive no maquinário.**

Uma ilustração parada é linha preta sobre off-white. Cor aparece em dois lugares
só: código em tela, porque tela é máquina rodando, e o que se move ou responde.
Nada mais, nunca. É isso que faz o acento significar alguma coisa.

Detalhe completo em `docs/ILLUSTRATION_SPEC.md`: tokens, a hachura a 45° como
única textura, contorno em vez de preenchimento, dois pesos de linha, e o
quality gate.

## O que ler para pegar contexto

Neste repo, nesta ordem: este arquivo, `docs/ILLUSTRATION_SPEC.md`, e o índice de
`docs/solutions/`. O contrato, o sistema, e as cicatrizes.

**Parte do material de trabalho não é versionada.** `docs/workspace.md` explica o
que fica de fora, por quê, e o que colocar em cada lugar se você estiver
recomeçando. Localmente isso inclui `reference/`, que tem o contexto do
portfólio em português, e `PROGRESS.md`, que tem o estado da sessão.

Instalado em `~/.claude/skills/`:

| Skill | Para quê |
|---|---|
| `oil-visual` | modelo estrutural da spec. Só o craft foi aproveitado |
| `oil-motion` | referência de animação. Ver a ressalva abaixo |

**Ressalva sobre o `oil-motion`:** ele resolve animação por geração de vídeo e
sprite atlas. A fase 2 aqui **não** vai por esse caminho. O critério do
`motion.md` exige que corpo, mesa e monitores sejam idênticos pixel a pixel entre
quadros, e nenhum método generativo entrega isso. A animação virou composição:
corpo estático, cabeça como camada que rotaciona, pupilas como formas que
transladam. Isso elimina o atlas, o orçamento de 240 frames e o custo de vídeo.

## Onde estamos

**Fase 1 fechada na primeira iteração completa.** O harness está de pé e o
primeiro asset está aprovado.

O que existe e foi exercitado de ponta a ponta:

- Adaptador com cinco backends. `fake` roda sem key e sem custo; `local` e
  `local-cn` rodam de verdade na máquina; `openai` e `gemini` chegam no serviço
  e são recusados por saldo, o que é estado de cobrança e não defeito de código.
- Geração local funcionando: mflux com Z-Image quantizado em 4 bits, pico de
  5,69 GB numa máquina de 16 GB, sem swap.
- `make check` com seis alvos, rodando em menos de meio segundo, incluindo
  fixtures quebrados de propósito para provar que cada check consegue reprovar.
- Onze lições em `docs/solutions/`, cada uma nomeando o que a garante.
- `hero-character` aprovado e congelado em `briefs/hero-character/approved/`,
  com recorte RGBA e a receita ao lado.

**O que a primeira iteração ensinou, em uma linha:** o sistema visual mudou três
vezes, e todas as três porque uma imagem mostrou que a spec estava errada, não o
contrário.

**Próximo passo:** a cena da mesa como asset separado, e depois a composição das
duas. O `briefs/hero-desk/brief.md` já existe e a primeira geração dele saiu em
perspectiva, que é o defeito a atacar.

**Dívida aberta:** este arquivo passou de 260 linhas contra o alvo de 100 de um
arquivo de entrada. Ele precisa virar roteador, com o detalhe migrando para
documentos temáticos. É o último item pendente do harness.

## Como trabalhar

- Um asset por vez. Mostre e espere.
- **Diga o que vai mudar antes de gerar, e espere.** Não encadeie gerações
  avisando depois. O feedback do Otávio é o portão que decide se segue ou não,
  e geração disparada sem ele combinada é decisão tomada no lugar dele. Uma
  rodada responde um conjunto de mudanças que ele viu escrito antes de rodar.
- Briefing antes de qualquer geração, sem exceção.
- Custo avisado antes de gastar.
- Nunca proponha trabalho manual de designer.
- Feedback honesto. O Otávio prefere avaliação direta a elogio.
- Se o resultado sair errado, o briefing é o primeiro suspeito.
- **Antes de escolher um modelo, cheque o `status` de cada flag da qual o
  desenho depende, não a existência dela.** Flag aceita e descartada em silêncio
  é o modo de falha mais caro aqui, porque parece prompt mal escrito. Medido em
  `docs/solutions/a-flag-can-exist-and-be-ignored.md`.
- **Backend que descarta negative prompt não segura sistema visual, mas pode
  propor um.** Sem o bloco negativo nada empurra contra a deriva do modelo, então
  ele não serve para manter o estilo estável. Serve para descobrir. Imagem que
  viola a spec é evidência sobre a spec tantas vezes quanto sobre a imagem, e
  quem decide qual é o Otávio, não o quality gate. Histórico em
  `docs/solutions/the-negative-block-was-carrying-the-style.md`.
- **O modelo não tem memória.** Cada geração recebe duas strings e nada mais:
  nem as imagens anteriores, nem o `## Acceptance`, nem a prosa da spec, nem
  esta conversa. Requisito que não está no prompt não chegou nele. Só seed, init
  image e LoRA atravessam de uma imagem para outra. Detalhe em
  `docs/solutions/the-model-has-no-memory.md`.
- **512 é para pergunta, 1024 é para candidato.** Uma rodada a 512 custa 92s e
  responde uma pergunta por vez, do tipo "essa mudança pegou". Nunca julgue
  semelhança, proporção, qualidade de linha, limpeza de fundo ou enquadramento
  a 512, e nunca promova uma imagem de 512 a candidata. Confirmou? Regenere a
  1024, e escolha como: se a imagem de origem **contradiz** a mudança, gere do
  zero, porque init image se herda e não se sobrescreve. Se não contradiz, parta
  dela com força alta. O porquê está em
  `docs/solutions/512-answers-some-questions-and-lies-about-others.md`.

## Fora de escopo, por decisão

**Treinar LoRA.** Decidido em 2026-09-07 por Otávio, e a razão importa mais que
a decisão: o valor deste projeto está no harness, no pipeline local com seus
parâmetros e na iteração guiada, e o foco declarado é uma UI consistente. LoRA
resolveria pose arbitrária, que é um problema que este projeto pode evitar
decidindo as poses de antemão, e custaria horas de setup, treino e validação
numa máquina de 16 GB, com resultado incerto.

O que substitui: uma biblioteca pequena de poses aprovadas, geradas do jeito que
o hero foi, congeladas como PNG e recompostas; e transformação de partes, cabeça,
braços, que ilustração chapada sem direção de luz aceita bem.

Reabrir só se aparecer um asset que exija pose nova e arbitrária, e mesmo assim
depois de contar quantos assets realmente exigem. Se voltar a ser considerado,
que seja como capítulo próprio do toolkit, por escolha, não fingindo que o
entregável exige.

## Decisões em aberto

- **Interface, para outras pessoas usarem.** Ideia do Otávio, para depois: campo
  de API key, um briefing solto que uma IA estrutura no formato daqui, botão de
  gerar, iteração de aprovar/reprovar, e então o briefing de animação e a
  geração de vídeo, com a grade de poses aparecendo como no demo do oil-motion.

  A arquitetura já aguenta: a UI seria camada por cima do `generate.py`, não uma
  reescrita. Dois cuidados quando chegar a hora:

  1. A IA que estrutura o briefing precisa receber a spec como contexto
     obrigatório e recusar briefing sem critério de aceite observável. O que faz
     o formato funcionar é ele forçar decisão, não o formato em si. Sem isso
     vira gerador de texto bonito e o problema só anda para a geração.
  2. Chave de API em interface hospedada significa pedir credencial paga de
     estranho num campo seu. Rodar local resolve e não custa nada.

- Backend local (MLX, Draw Things) no M-series: adiar, não descartar. Serve para
  iterar, não para render final. Reavaliar com o adaptador já pronto.
- O `zenmux.py` nunca foi executado. O endpoint e o formato de resposta são
  suposição baseada em compatibilidade com OpenAI, e precisam de um teste real
  antes de qualquer confiança.
- A tirinha de três cenas: morph contínuo por vídeo (rota B) ou três cortes.
  Decidir na fase 2, com o custo real na mão.
