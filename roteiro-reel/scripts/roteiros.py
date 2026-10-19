"""Organiza a pasta de roteiros: cria um roteiro novo no formato certo, lista o que existe, muda o estado e
gera o arte.json da Edita reel a partir do roteiro.

Uso:
    python roteiros.py novo   PASTA "Título do roteiro" [--data 2026-10-25]
    python roteiros.py lista  PASTA [--estado aprovado]
    python roteiros.py estado PASTA ARQUIVO.md roteiro|aprovado|gravado|descartado
    python roteiros.py arte   PASTA ARQUIVO.md [--rede instagram|tiktok] [--saida arte.json]

Só Python puro, nada pra instalar. O formato do arquivo está em references/modelo-roteiro.md.
"""
import argparse
import json
import os
import re
import sys
import unicodedata
from datetime import date

ESTADOS = ["roteiro", "aprovado", "gravado", "descartado"]
PALAVRAS_POR_SEGUNDO = 2.5          # cerca de 150 palavras por minuto: é estimativa, cada pessoa fala num ritmo
CAMPOS = ["titulo", "estado", "tipo", "funil", "formato", "duracao_alvo", "palavra", "capa", "criado"]
SECOES_MODELO = [
    ("Tese", "(A ideia central em uma frase.)"),
    ("Capas", "(5 opções, da mais forte pra mais suave, com a recomendada marcada.)"),
    ("Fala", "(O roteiro em prosa contínua, sem rótulo de batida, do jeito que vai ser dito.)"),
    ("Na tela", '(Uma linha por coisa que aparece: - quando eu falar "palavra": o que aparece (arquivo: prints/x.png))'),
    ("Legenda Instagram", "(Gancho na primeira linha, corpo curto, chamada.)"),
    ("Legenda TikTok", "(Curta, sem palavra-chave.)"),
    ("Legenda LinkedIn", "(Gancho de uma linha, parágrafos curtos.)"),
    ("Fontes", "(O link de cada dado citado.)"),
    ("Notas", "(O que ficou [CONFERIR] e por quê.)"),
]


# ------------------------------------------------------------ ler e escrever
def ler(caminho):
    """Devolve (cabeçalho, seções) de um arquivo de roteiro. Seções em ordem, texto sem as linhas em branco das pontas."""
    t = open(caminho, encoding="utf-8").read()
    meta, corpo = {}, t
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n?", t, re.S)
    if m:
        for linha in m.group(1).splitlines():
            if ":" in linha:
                k, v = linha.split(":", 1)
                meta[k.strip()] = v.strip()
        corpo = t[m.end():]
    secoes = {}
    for bloco in re.split(r"(?m)^## ", "\n" + corpo)[1:]:
        nome, _, texto = bloco.partition("\n")
        secoes[nome.strip()] = texto.strip()
    return meta, secoes


def vazio(texto):
    """Seção vazia ou ainda com o texto-guia do modelo (entre parênteses)."""
    t = (texto or "").strip()
    return not t or (t.startswith("(") and t.endswith(")") and "\n" not in t)


def escrever(caminho, meta, secoes):
    linhas = ["---"] + [f"{k}: {meta.get(k, '')}".rstrip() for k in CAMPOS] + \
             [f"{k}: {v}" for k, v in meta.items() if k not in CAMPOS] + ["---", ""]
    for nome, texto in secoes.items():
        linhas += [f"## {nome}", texto, ""]
    open(caminho, "w", encoding="utf-8").write("\n".join(linhas))


def slug(txt):
    s = unicodedata.normalize("NFD", txt.lower())
    s = "".join(c for c in s if not unicodedata.combining(c))
    return re.sub(r"[^a-z0-9]+", "-", s).strip("-")[:60] or "roteiro"


def palavras_da_fala(secoes):
    fala = secoes.get("Fala", "")
    return 0 if vazio(fala) else len(re.findall(r"\w+", fala))


def duracao_estimada(secoes):
    return round(palavras_da_fala(secoes) / PALAVRAS_POR_SEGUNDO)


def roteiros(pasta):
    out = []
    for f in sorted(os.listdir(pasta)):
        if f.endswith(".md") and re.match(r"\d{4}-\d{2}-\d{2}-", f):
            meta, sec = ler(os.path.join(pasta, f))
            out.append((f, meta, sec))
    return out


# ------------------------------------------------------------ "Na tela" vira arte.json
def itens_na_tela(texto, pasta):
    itens = []
    if vazio(texto):
        return itens
    for linha in texto.splitlines():
        linha = linha.strip().lstrip("-*").strip()
        if not linha:
            continue
        gat = re.search(r'["“]([^"”]+)["”]', linha)
        arq = re.search(r"\(arquivo:\s*([^)]+)\)", linha)
        descricao = re.sub(r'^quando eu falar\s*["“][^"”]+["”]\s*:?\s*', "", linha, flags=re.I)
        descricao = re.sub(r"\(arquivo:[^)]+\)", "", descricao).strip(" .")
        itens.append({"gatilho": gat.group(1).strip() if gat else None,
                      "arquivo": os.path.join(pasta, arq.group(1).strip()) if arq else None,
                      "descricao": descricao})
    return itens


def montar_arte(meta, secoes, pasta, rede):
    arte = {"titulo": meta.get("titulo", ""), "legenda": "ativa"}
    if meta.get("capa"):
        arte["capa"] = {"texto": meta["capa"]}
    inserts, numeros, listas, avisos = [], [], [], []
    for it in itens_na_tela(secoes.get("Na tela", ""), pasta):
        if not it["gatilho"]:
            avisos.append(f"Sem palavra-gatilho entre aspas, ficou de fora: {it['descricao']}")
            continue
        primeira = it["gatilho"].split()[0]          # a arte entra quando a primeira palavra do gatilho é dita
        de = {"palavra": primeira}
        ate = {"palavra": primeira, "mais": 3.0}
        if it["arquivo"]:
            if not os.path.exists(it["arquivo"]):
                avisos.append(f"Arquivo não encontrado: {it['arquivo']}")
            inserts.append({"imagem": it["arquivo"], "de": de, "ate": ate, "x": 160, "y": 760, "largura": 760, "credito": ""})
            avisos.append(f"Preencha o crédito (de onde veio a imagem) do insert de \"{it['gatilho']}\"")
        elif it["descricao"].lower().startswith("lista:"):
            itens = [x.strip() for x in it["descricao"][6:].split(",") if x.strip()]
            listas.append({"itens": itens, "de": de, "ate": {"palavra": primeira, "mais": 2.0 + 1.5 * len(itens)},
                           "marcos": [{"palavra": x.split()[0]} for x in itens]})
        else:
            num = re.search(r"\d+(?:[.,]\d+)?%?", it["descricao"])
            if num:
                rot = re.search(r"r[óo]tulo\s*[\"“]?([^\"”]+)", it["descricao"])
                numeros.append({"numero": num.group(0), "rotulo": rot.group(1).strip() if rot else "", "de": de, "ate": ate})
            else:
                avisos.append(f"Não sei desenhar isso sozinha, ficou de fora: {it['descricao']}")
    if inserts:
        arte["inserts"] = inserts
    if numeros:
        arte["numeros"] = numeros
    if listas:
        arte["listas"] = listas
    palavra = meta.get("palavra", "").strip()
    if rede == "tiktok":
        arte["fecho"] = {"texto": "Salva esse vídeo e me segue"}
    else:
        arte["fecho"] = {"texto": f"Comenta {palavra.upper()}" if palavra else "Salva esse vídeo"}
    return arte, avisos


# ------------------------------------------------------------ comandos
def cmd_novo(a):
    os.makedirs(a.pasta, exist_ok=True)
    dia = a.data or date.today().isoformat()
    caminho = os.path.join(a.pasta, f"{dia}-{slug(a.titulo)}.md")
    if os.path.exists(caminho):
        sys.exit(f"Já existe: {caminho}")
    meta = {"titulo": a.titulo, "estado": "roteiro", "criado": dia}
    escrever(caminho, meta, dict(SECOES_MODELO))
    print(caminho)


def cmd_lista(a):
    rs = [r for r in roteiros(a.pasta) if not a.estado or r[1].get("estado") == a.estado]
    if not rs:
        print("Nenhum roteiro" + (f" com estado {a.estado}" if a.estado else "") + f" em {a.pasta}")
        return
    print(f"{'estado':10s} {'tipo':9s} {'funil':6s} {'dur':>5s}  título  (arquivo)")
    for f, meta, sec in rs:
        d = duracao_estimada(sec)
        print(f"{meta.get('estado', ''):10s} {meta.get('tipo', ''):9s} {meta.get('funil', ''):6s} {str(d) + 's' if d else '':>5s}  "
              f"{meta.get('titulo', '')}  ({f})")
    ativos = [m for _, m, _ in rs if m.get("estado") in ("roteiro", "aprovado")]
    if ativos:
        conta = lambda campo, v: sum(1 for m in ativos if m.get(campo, "").lower().startswith(v))
        print(f"\nNa fila ({len(ativos)}): valor {conta('tipo', 'valor')}, opinião {conta('tipo', 'opini')}, impacto {conta('tipo', 'impacto')}"
              f" | topo {conta('funil', 'topo')}, meio {conta('funil', 'meio')}, fundo {conta('funil', 'fundo')}")


def cmd_estado(a):
    caminho = a.arquivo if os.path.isabs(a.arquivo) else os.path.join(a.pasta, a.arquivo)
    meta, sec = ler(caminho)
    meta["estado"] = a.novo
    escrever(caminho, meta, sec)
    print(f"{os.path.basename(caminho)}: {a.novo}")


def cmd_arte(a):
    caminho = a.arquivo if os.path.isabs(a.arquivo) else os.path.join(a.pasta, a.arquivo)
    meta, sec = ler(caminho)
    arte, avisos = montar_arte(meta, sec, os.path.abspath(a.pasta), a.rede)
    saida = a.saida or os.path.splitext(caminho)[0] + (f"-arte-{a.rede}.json" if a.rede != "instagram" else "-arte.json")
    json.dump(arte, open(saida, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(saida)
    for x in avisos:
        print("  aviso:", x)


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("novo"); p.add_argument("pasta"); p.add_argument("titulo"); p.add_argument("--data")
    p = sub.add_parser("lista"); p.add_argument("pasta"); p.add_argument("--estado", choices=ESTADOS)
    p = sub.add_parser("estado"); p.add_argument("pasta"); p.add_argument("arquivo"); p.add_argument("novo", choices=ESTADOS)
    p = sub.add_parser("arte"); p.add_argument("pasta"); p.add_argument("arquivo")
    p.add_argument("--rede", choices=["instagram", "tiktok"], default="instagram"); p.add_argument("--saida")
    a = ap.parse_args()
    {"novo": cmd_novo, "lista": cmd_lista, "estado": cmd_estado, "arte": cmd_arte}[a.cmd](a)


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    main()
