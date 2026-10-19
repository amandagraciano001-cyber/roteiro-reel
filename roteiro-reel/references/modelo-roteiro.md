# Formato do arquivo de roteiro

Cada roteiro é um arquivo `AAAA-MM-DD-titulo.md` na pasta de roteiros. O `roteiros.py novo` cria ele já neste formato. O cabeçalho entre os `---` tem uma informação por linha; o resto são seções que começam com `## `. Os scripts leem as duas coisas, então mantenha os nomes das seções.

```markdown
---
titulo: Planilha ainda ganha de app
estado: roteiro
tipo: opinião
funil: topo
formato: tese pra câmera
duracao_alvo: 60
palavra:
capa: Seu app não organiza nada
criado: 2026-10-19
---

## Tese
Pra quem está começando um negócio, uma planilha bem feita organiza mais que qualquer app.

## Capas
1. Seu app não organiza nada (recomendada: contra o senso comum, e o vídeo prova)
2. Planilha ganha de app
3. O app que eu desinstalei
4. Pare de baixar app de gestão
5. Você não precisa de mais app

## Fala
Eu desinstalei três apps de gestão esse ano. E o negócio ficou mais organizado...

## Na tela
- quando eu falar "planilha": print da minha planilha de caixa (arquivo: prints/planilha.png)
- quando eu falar "três apps": número 3 com o rótulo "apps desinstalados"

## Legenda Instagram
Eu desinstalei três apps de gestão esse ano.

## Legenda TikTok
Planilha ainda ganha de app. Salva esse vídeo.

## Legenda LinkedIn
Desinstalei três apps de gestão este ano.

## Fontes
- (link de cada dado citado, aberto e conferido)

## Notas
- [CONFERIR] (o que não deu pra confirmar e por quê)
```

## Os campos do cabeçalho

| Campo | O que vai |
|---|---|
| `titulo` | Nome interno do roteiro |
| `estado` | `roteiro`, `aprovado`, `gravado` ou `descartado` |
| `tipo` | `valor`, `opinião` ou `impacto` |
| `funil` | `topo`, `meio` ou `fundo` |
| `formato` | Lista, tese pra câmera, história, tela curta, notícia |
| `duracao_alvo` | Segundos |
| `palavra` | A palavra-chave (vazio em topo de funil) |
| `capa` | A capa que a pessoa escolheu |
| `criado` | A data de criação |

## "Na tela"

Uma linha por coisa que aparece. O que está entre aspas é a palavra da fala que faz a arte entrar; o que está em `(arquivo: ...)` é a imagem, relativa à pasta de roteiros. Sem arquivo, a linha vira número ou lista na arte, conforme o texto.
