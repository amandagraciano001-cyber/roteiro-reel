# Roteiro reel

Uma skill gratuita pro Claude Code e pro Codex que escreve o roteiro do seu reel falado na sua voz, antes de você ligar a câmera.

Você manda uma ideia, uma notícia ou um vídeo que viu e gostou, chama `/roteiro-reel` (ou `$roteiro-reel` no Codex) e o agente:

1. **Aprende a sua voz** na primeira vez: sete perguntas, uma de cada vez, e guarda um `voz.md` com o seu jeito de falar, o que você vende e o que você nunca diria.
2. **Acha a tese** em uma frase e classifica o vídeo (ensina, opina ou emociona; atrai, gera confiança ou vende).
3. **Confere os fatos**: todo número e todo nome vem de uma fonte aberta. O que não confirma, sai ou fica marcado pra você conferir.
4. **Escreve o roteiro** numa estrutura de 7 batidas que prende do começo ao fim, em fala contínua, pronta pra ler.
5. **Propõe 5 capas** pro primeiro segundo, critica cada uma e recomenda uma. Quem escolhe é você.
6. **Escreve a legenda de cada rede**: Instagram com palavra-chave, TikTok e Shorts sem, LinkedIn no tom de lá.
7. **Monta o dia de gravação**: uma página com todos os roteiros aprovados e um teleprompter em tela cheia, que rola sozinho.

Adaptando um vídeo de outra pessoa, ele mantém a estrutura que funcionou e troca tudo o que é da vida dela pelo que é seu. Nunca copia frase inteira.

Feita por [Amanda Graciano](https://amandagraciano.com), a partir do processo que ela usa pra escrever os próprios roteiros.

## Funciona em

Claude Code e Codex, no Mac, no Windows e no Linux. O instalador acha sozinho qual agente você tem e coloca a skill no lugar certo de cada um.

| Agente | Onde a skill fica | Como chamar |
|---|---|---|
| Claude Code | `~/.claude/skills/roteiro-reel` | `/roteiro-reel` |
| Codex | `~/.agents/skills/roteiro-reel` | `$roteiro-reel` |

## O que você precisa

- [Claude Code](https://claude.com/claude-code) ou [Codex](https://developers.openai.com/codex)

| | Mac | Windows | Linux |
|---|---|---|---|
| Python 3.9 ou mais novo | já vem no Mac (ou `brew install python`) | `winget install Python.Python.3.12` | `sudo apt install python3 python3-venv` |

## Como instalar

**Jeito mais fácil:** abra o Claude Code ou o Codex e cole:

```
https://github.com/amandagraciano001-cyber/roteiro-reel

Instala essa skill pra mim e confere se as dependências estão instaladas.
```

**Pelo instalador.** Baixe o repositório (com o `git clone` abaixo, ou pelo botão Code > Download ZIP aqui no GitHub) e rode o instalador dentro da pasta.

Mac ou Linux, no Terminal:

```bash
git clone https://github.com/amandagraciano001-cyber/roteiro-reel.git
cd roteiro-reel
bash instalar.sh
```

Windows, no PowerShell:

```powershell
git clone https://github.com/amandagraciano001-cyber/roteiro-reel.git
cd roteiro-reel
powershell -ExecutionPolicy Bypass -File instalar.ps1
```

Pra instalar só num agente: `--claude` ou `--codex` no Mac e no Linux, `-Claude` ou `-Codex` no Windows. Já tinha instalado? Rode o instalador de novo: ele troca os arquivos e mantém o que já foi baixado.

## Como usar

No Claude Code a skill é chamada com `/roteiro-reel`; no Codex, com `$roteiro-reel`. O resto do pedido é igual.

```
/roteiro-reel quero falar que planilha ainda ganha de app de gestão pra quem está começando um negócio
```

```
/roteiro-reel adapta esse vídeo pra mim: (cola a transcrição)
```

```
/roteiro-reel me dá 5 ideias pra semana que vem
```

```
/roteiro-reel monta o dia de gravação
```

Na primeira vez ele pergunta onde guardar os roteiros e faz a entrevista da voz.

## A família

Roteiro reel é a primeira de três skills que funcionam juntas, cada uma sozinha também:

1. **Roteiro reel** (esta): antes de gravar. Ideia entra, roteiro sai.
2. **[Edita reel](https://github.com/amandagraciano001-cyber/edita-reel)**: depois de gravar. Vídeo bruto entra, reel editado sai. O roteiro vira a arte da edição com um comando (`roteiros.py arte`).
3. **[Estúdio reel](https://github.com/amandagraciano001-cyber/estudio-reel)**: depois de editar. Os vídeos prontos viram fila, calendário e histórico. O Estúdio lê o título, as legendas e a palavra-chave direto do roteiro.

## O que vem em cada arquivo

| Arquivo | O que faz |
|---|---|
| `instalar.sh` e `instalar.ps1` | Os instaladores do Mac e Linux e do Windows |
| `roteiro-reel/agents/openai.yaml` | O nome e a descrição que o Codex mostra |
| `roteiro-reel/SKILL.md` | O passo a passo que o agente segue |
| `references/estrutura.md` | As 7 batidas, o arco de opinião, os gatilhos de compartilhamento, tipo, funil e duração |
| `references/ganchos.md` | As famílias de gancho e capa, e como escolher |
| `references/redes.md` | O que muda no Instagram, TikTok, Shorts e LinkedIn |
| `references/voz-modelo.md` | O modelo do `voz.md` |
| `references/modelo-roteiro.md` | O formato do arquivo de roteiro |
| `scripts/roteiros.py` | Cria, lista e muda o estado dos roteiros; gera o `arte.json` da Edita reel |
| `scripts/gravacao.py` | A página do dia de gravação, com teleprompter |

## Licença

MIT. Use, adapte e compartilhe.
