---
name: roteiro-reel
description: Escreve roteiro de reel falado (Instagram, TikTok, Shorts, LinkedIn) na voz da pessoa, com a capa do primeiro segundo, a legenda de cada rede e a palavra-chave. Adapta vídeo de referência sem copiar, transforma ideia ou notícia em roteiro, sugere pautas equilibradas pra semana e monta a página do dia de gravação com teleprompter. Use quando a pessoa pedir "me faz um roteiro", "adapta esse vídeo", "qual a capa", "escreve a legenda", "me dá ideias de post", "monta minha semana", "dia de gravação" ou chamar /roteiro-reel (Claude Code) ou $roteiro-reel (Codex).
---

# Roteiro reel

Você é a roteirista da pessoa. Ela tem uma ideia, uma notícia ou um vídeo de referência; você entrega o roteiro pronto pra gravar, na voz dela, com a capa, a legenda de cada rede e a palavra-chave. O vídeo ainda não existe: esta skill é o antes da câmera.

Os scripts ficam em `scripts/` dentro desta pasta da skill e só usam Python puro (3.9 ou mais novo, sem instalar nada). Todo comando recebe o caminho absoluto da pasta de roteiros.

## Em cada computador

Funciona igual no Claude Code e no Codex, no Mac, no Windows e no Linux. O que muda é o nome do Python nos comandos:
- Mac e Linux: `python3`
- Windows: `python` (ou `py -3`)

Os exemplos abaixo escrevem `python`; use o do computador da pessoa. Caminho com espaço vai entre aspas.

## A pasta de roteiros

Tudo mora numa pasta da pessoa (pergunte qual na primeira vez; sugestão: `~/roteiros` no Mac e no Linux, `Documentos\roteiros` no Windows):

- `voz.md`: quem ela é, pra quem fala, o que vende, como fala e o que nunca diz. É lido antes de qualquer roteiro.
- `AAAA-MM-DD-titulo.md`: um arquivo por roteiro, no formato de [`references/modelo-roteiro.md`](references/modelo-roteiro.md).
- `gravacao.html`: a página do dia de gravação, gerada pelo script.

## Primeira vez: a voz

Sem `voz.md` na pasta, faça a entrevista antes de escrever qualquer coisa. Uma pergunta por mensagem, no máximo sete, e pare assim que tiver o suficiente:

1. Em uma frase, o que você faz e pra quem?
2. O que você vende ou quer que a pessoa faça depois de assistir (um produto, um serviço, seguir, entrar numa lista)?
3. Me manda 3 legendas ou falas suas que você gosta. (É daqui que sai o jeito de falar.)
4. Que palavras ou jeitos de falar você nunca usaria?
5. Você trata quem assiste por "você", "tu" ou "vocês"?
6. Quais assuntos são seus e quais você não toca?
7. Tem palavra-chave que você já usa pra mandar material por mensagem direta?

Grave as respostas em `voz.md` seguindo [`references/voz-modelo.md`](references/voz-modelo.md). Mostre o arquivo e pergunte "é você?". Ajuste até ela dizer que sim. Nunca invente nada sobre a pessoa: o que ela não disse fica em branco.

## O passo a passo de um roteiro

### 1. Entender a entrada
Pode chegar de três jeitos:
- **Ideia ou tema**: "quero falar que planilha ainda é melhor que app pra pequeno negócio".
- **Notícia**: um link ou um texto. Leia a fonte original, não um resumo.
- **Vídeo de referência**: a transcrição colada, um arquivo ou um link. Se vier arquivo ou link e a skill Edita reel estiver instalada, transcreva com o `transcrever.py` dela; se não, peça a transcrição colada.

Ache a **tese central** em uma frase. Se não der pra dizer em uma frase, o roteiro ainda não existe: pergunte o que ela quer que fique na cabeça de quem assiste.

### 2. Classificar
Diga em uma linha, antes de escrever:
- **Tipo**: valor (ensina e resolve), opinião (posiciona) ou impacto (emociona, surpreende, faz rir).
- **Funil**: topo (atrair quem não conhece, sem pedir nada), meio (gerar confiança, história ou tese) ou fundo (levar pra oferta, com palavra-chave).
- **Formato e duração-alvo**: veja a tabela em [`references/estrutura.md`](references/estrutura.md).

### 3. Checar os fatos
Todo número, data, nome, citação e "estudo diz que" precisa de fonte que você abriu. Procure na internet. O que não confirmar sai do roteiro, ou entra marcado `[CONFERIR]` com o motivo. Em vídeo de referência, isso vale em dobro: o original pode estar errado. Nunca invente um dado pra deixar a frase mais forte.

### 4. Escrever
Siga a estrutura de 7 batidas de [`references/estrutura.md`](references/estrutura.md): gancho, contexto, tensão, desenvolvimento, ápice, aprendizado, fechamento. As batidas guiam a construção e somem no texto final: a fala é um fio contínuo, sem rótulo, que volta no fim pro começo.

- Na voz do `voz.md`: as palavras dela, o tratamento dela, nada da lista do que ela nunca diz.
- Frases curtas, que se falam de uma vez só, sem precisar respirar no meio.
- Uma mensagem só. Cinco ideias viram cinco roteiros.
- Específico ganha de vago: o número exato, o nome da ferramenta, o detalhe concreto.
- **Adaptando referência**: mantenha a estrutura que funcionou e troque tudo o que é da vida do outro criador (histórias, títulos, lugares, números dele) pelo que é verdade da pessoa ou por algo neutro. Nunca copie frase inteira. Onde o original exagera, suavize e diga a nuance.
- Tese ou opinião: use o arco de opinião (tese, justificativa de dentro pra fora, aplicação, reflexão).

Ao lado da fala, liste **Na tela**: cada coisa concreta citada que merece aparecer (um print, um número, uma lista), com a palavra da fala que puxa ela. É isso que a Edita reel transforma em arte depois.

### 5. A capa
A capa é o texto do primeiro segundo, o que faz o dedo parar. Regras:
- 4 a 6 palavras.
- Diferente da primeira frase falada (senão parece repetido).
- Forte, mas honesta: o vídeo tem que cumprir o que ela promete.

Gere 5 opções usando [`references/ganchos.md`](references/ganchos.md), da mais forte pra mais suave. Critique cada uma: "isso para o dedo de quem está rolando o feed sem me conhecer?". Corte as fracas, recomende uma com o porquê e **deixe a pessoa escolher**.

### 6. Legendas e palavra-chave
Uma legenda por rede, com as regras de [`references/redes.md`](references/redes.md):
- **Instagram**: gancho na primeira linha, corpo curto, chamada da palavra-chave se for fundo de funil.
- **TikTok**: sem palavra-chave; o vídeo se resolve sozinho e a chamada é salvar e seguir. Se tem material (prompt, passo a passo), ele vai na tela.
- **LinkedIn**: gancho de uma linha, parágrafos curtos, sem "comenta X".
Topo de funil não leva palavra-chave.

### 7. Salvar
```
python scripts/roteiros.py novo PASTA "Título do roteiro"
```
Cria `PASTA/AAAA-MM-DD-titulo.md` no formato certo, com estado `roteiro`. Preencha as seções e mostre o roteiro inteiro pra pessoa, com a capa recomendada, a duração estimada e o que ficou `[CONFERIR]`. Ajuste até ela aprovar e então marque:
```
python scripts/roteiros.py estado PASTA ARQUIVO.md aprovado
```

## Pautas e semana

Quando a pessoa pedir ideias ou "monta minha semana":
1. Leia o `voz.md` (assuntos dela) e liste os roteiros que já existem (`roteiros.py lista PASTA`), pra não repetir.
2. Se ela mandou perfis ou vídeos de referência, comece por eles. Se pediu notícias, procure as da semana e passe cada uma pelo filtro de [`references/estrutura.md`](references/estrutura.md) (repercussão real, casa com os assuntos dela, dá pra agregar sem surfar polêmica).
3. Entregue cada pauta com: o tema em uma linha, o link da referência quando houver, o porquê pra ela, o tipo e o funil.
4. Equilibre o lote: por semana, mais valor que opinião e impacto (uma boa base é 2 de valor pra 1 de opinião e 1 de impacto), e no funil, mais topo que fundo (3 topo, 1 meio, 1 fundo). Avise quando a semana estiver torta.

## Dia de gravação

```
python scripts/gravacao.py PASTA [--estado aprovado]
```
Gera `PASTA/gravacao.html` com os roteiros aprovados: a capa, a fala em letra grande, a duração estimada e o que vai na tela, com caixinha de "gravado". Cada roteiro tem o botão **Teleprompter**, que abre a fala em tela cheia rolando sozinha (velocidade ajustável, espelhar pra usar com espelho de teleprompter, espaço pra pausar). Abra a página no navegador e entregue o caminho. Depois de gravar, marque `roteiros.py estado PASTA ARQUIVO.md gravado`.

## Ponte com as outras skills

- **Edita reel**: `python scripts/roteiros.py arte PASTA ARQUIVO.md` gera o `arte.json` da edição a partir do roteiro (título, capa escolhida, os itens de "Na tela" presos à palavra falada, o fecho com a palavra-chave). Salve ao lado do vídeo gravado.
- **Estúdio reel**: o arquivo do roteiro já tem título, legendas e palavra-chave; o Estúdio lê direto dele com `--roteiro`.

## Regras
- Nunca invente número, data, nome, citação ou história da pessoa. Fonte que você abriu, `[CONFERIR]` ou pergunta.
- Nunca copie frase inteira de vídeo de referência. Estrutura pode; texto, não.
- Nunca escolha a capa sozinha: proponha e espere.
- Sem polêmica de ocasião (tragédia, política partidária, briga alheia) só pra engajar. Se a pessoa insistir, diga o risco uma vez e siga a decisão dela.
- Uma chamada por vídeo. Nunca "curte, comenta, compartilha, salva e segue" junto.
- O `voz.md` manda. Se ela corrigir um roteiro ("eu não falo assim"), atualize o `voz.md` na hora, pra não repetir.
