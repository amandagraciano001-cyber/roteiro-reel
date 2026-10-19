"""Monta a página do dia de gravação: os roteiros aprovados, cada um com a capa, a fala em letra grande, a
duração estimada, o que vai na tela e um teleprompter em tela cheia.

Uso:
    python gravacao.py PASTA [--estado aprovado|roteiro|todos] [--saida gravacao.html]

Abra PASTA/gravacao.html no navegador. No teleprompter: espaço pausa e continua, setas mudam a velocidade,
+ e - mudam o tamanho da letra, E espelha (pra espelho de teleprompter), Esc fecha. O "gravado" que você marca
fica salvo neste navegador. Nada sai do seu computador.
"""
import argparse
import sys
import html
import json
import os
from datetime import date

from roteiros import duracao_estimada, itens_na_tela, roteiros, vazio

CSS = """
:root{--fundo:#f5f5f2;--cartao:#fff;--tinta:#15171c;--suave:rgba(21,23,28,.58);--linha:rgba(21,23,28,.12);--cor:#2f5bea;--ok:#1d8a4e}
@media(prefers-color-scheme:dark){:root{--fundo:#0d0f14;--cartao:#161922;--tinta:#eef0f5;--suave:rgba(238,240,245,.6);--linha:rgba(238,240,245,.12);--cor:#7c9cff;--ok:#4cc38a}}
*{box-sizing:border-box;margin:0;padding:0}body{font-family:-apple-system,Inter,Segoe UI,sans-serif;background:var(--fundo);color:var(--tinta);padding:36px 18px 90px}
.wrap{max-width:860px;margin:0 auto}h1{font-size:34px;letter-spacing:-.03em}.sub{color:var(--suave);margin:6px 0 26px;line-height:1.5}
.r{background:var(--cartao);border:1px solid var(--linha);border-radius:20px;padding:22px;margin-bottom:18px}.r.feito{opacity:.55}
.topo{display:flex;justify-content:space-between;gap:12px;align-items:flex-start}.n{font-size:13px;font-weight:700;color:var(--cor)}
h2{font-size:15px;font-weight:600;color:var(--suave);margin:2px 0 10px}.capa{font-size:30px;font-weight:800;letter-spacing:-.02em;line-height:1.1;margin-bottom:12px}
.tags{display:flex;flex-wrap:wrap;gap:6px;margin-bottom:16px}.tag{font-size:12px;font-weight:600;padding:4px 10px;border-radius:999px;background:var(--fundo);color:var(--suave);border:1px solid var(--linha)}
.fala{font-size:21px;line-height:1.6}.fala p{margin-bottom:12px}
.tela{margin-top:14px;padding-top:12px;border-top:1px dashed var(--linha);font-size:14px;color:var(--suave)}.tela li{margin:4px 0 0 18px}
.acoes{display:flex;gap:8px;flex-wrap:wrap;margin-top:16px}button{font:inherit;font-size:14px;font-weight:600;padding:10px 16px;border-radius:11px;border:1px solid var(--linha);background:var(--cartao);color:var(--tinta);cursor:pointer}
button.prim{background:var(--cor);border-color:var(--cor);color:#fff}button.on{background:var(--ok);border-color:var(--ok);color:#fff}
#tp{position:fixed;inset:0;background:#000;color:#fff;display:none;z-index:9;overflow:hidden}#tp.aberto{display:block}
#tp .txt{position:absolute;left:8%;right:8%;top:0;font-size:56px;line-height:1.45;font-weight:600;will-change:transform}
#tp .txt p{margin-bottom:.8em}#tp .guia{position:absolute;left:0;right:0;top:38%;height:2px;background:rgba(255,255,255,.18)}
#tp .barra{position:absolute;left:0;right:0;bottom:0;display:flex;gap:10px;align-items:center;justify-content:center;padding:14px;background:linear-gradient(transparent,rgba(0,0,0,.9));font-size:14px;color:rgba(255,255,255,.75)}
#tp .barra button{background:rgba(255,255,255,.12);border-color:rgba(255,255,255,.2);color:#fff;padding:8px 12px}#tp.espelho .txt{transform-origin:center;scale:-1 1}
@media(max-width:640px){.capa{font-size:24px}.fala{font-size:18px}#tp .txt{font-size:38px}}
"""

JS = """
const K='gravacao-feitos';function feitos(){try{return JSON.parse(localStorage.getItem(K)||'{}')}catch(e){return {}}}
function marca(id){const f=feitos();f[id]=!f[id];try{localStorage.setItem(K,JSON.stringify(f))}catch(e){}pinta()}
function pinta(){const f=feitos();let n=0;document.querySelectorAll('.r').forEach(r=>{const ok=!!f[r.dataset.id];if(ok)n++;r.classList.toggle('feito',ok);
 const b=r.querySelector('.gv');b.classList.toggle('on',ok);b.textContent=ok?'Gravado ✓':'Marcar como gravado'});
 document.getElementById('conta').textContent=n+' de '+document.querySelectorAll('.r').length+' gravados'}
let vel=+(localStorage.getItem('tp-vel')||40),tam=+(localStorage.getItem('tp-tam')||56),y=0,rodando=false,ult=0;
const tp=document.getElementById('tp'),txt=tp.querySelector('.txt');
function abre(id){txt.innerHTML=document.getElementById('fala-'+id).innerHTML;y=innerHeight*.38;rodando=false;tp.classList.add('aberto');aplica();info()}
function fecha(){tp.classList.remove('aberto');rodando=false}
function aplica(){txt.style.fontSize=tam+'px';txt.style.transform='translateY('+y+'px)'}
function info(){tp.querySelector('.st').textContent=(rodando?'rodando':'pausado')+' · velocidade '+vel+' · letra '+tam}
function passo(t){if(rodando&&tp.classList.contains('aberto')){y-=vel*(t-ult)/1000;if(y<-txt.offsetHeight+innerHeight*.3)rodando=false;aplica()}ult=t;requestAnimationFrame(passo)}
requestAnimationFrame(passo);
function joga(){rodando=!rodando;info()}function velo(d){vel=Math.max(5,Math.min(200,vel+d));try{localStorage.setItem('tp-vel',vel)}catch(e){}info()}
function letra(d){tam=Math.max(24,Math.min(120,tam+d));try{localStorage.setItem('tp-tam',tam)}catch(e){}aplica();info()}
function espelha(){tp.classList.toggle('espelho')}function volta(){y=innerHeight*.38;aplica()}
addEventListener('keydown',e=>{if(!tp.classList.contains('aberto'))return;if(e.key===' '){e.preventDefault();joga()}else if(e.key==='Escape')fecha();
 else if(e.key==='ArrowUp')velo(5);else if(e.key==='ArrowDown')velo(-5);else if(e.key==='+'||e.key==='=')letra(4);else if(e.key==='-')letra(-4);
 else if(e.key==='e'||e.key==='E')espelha();else if(e.key==='Home')volta()});
tp.addEventListener('wheel',e=>{y-=e.deltaY;aplica()},{passive:true});pinta();
"""


def paragrafos(texto):
    return "".join(f"<p>{html.escape(p.strip())}</p>" for p in texto.split("\n") if p.strip())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("pasta")
    ap.add_argument("--estado", default="aprovado", help="aprovado (padrão), roteiro ou todos")
    ap.add_argument("--saida")
    a = ap.parse_args()
    pasta = os.path.abspath(a.pasta)
    rs = [r for r in roteiros(pasta)
          if (a.estado == "todos" and r[1].get("estado") != "descartado") or r[1].get("estado") == a.estado]
    e = html.escape
    blocos, total = [], 0
    for k, (f, meta, sec) in enumerate(rs, 1):
        if vazio(sec.get("Fala")):
            continue
        d = duracao_estimada(sec)
        total += d
        tela = "".join(f"<li>{e(('“' + i['gatilho'] + '”: ') if i['gatilho'] else '')}{e(i['descricao'])}</li>"
                       for i in itens_na_tela(sec.get("Na tela", ""), pasta))
        tags = "".join(f'<span class="tag">{e(v)}</span>' for v in (meta.get("tipo"), meta.get("funil"), meta.get("formato"),
                                                                     f"cerca de {d} s" if d else None,
                                                                     f"palavra {meta['palavra']}" if meta.get("palavra") else None) if v)
        rid = e(f)
        blocos.append(f"""<div class="r" data-id="{rid}"><div class="topo"><div><div class="n">{k:02d}</div><h2>{e(meta.get('titulo', ''))}</h2></div></div>
<div class="capa">{e(meta.get('capa') or '(capa ainda não escolhida)')}</div><div class="tags">{tags}</div>
<div class="fala" id="fala-{rid}">{paragrafos(sec['Fala'])}</div>
{f'<div class="tela"><b>Na tela</b><ul>{tela}</ul></div>' if tela else ''}
<div class="acoes"><button class="prim" onclick="abre('{rid}')">Teleprompter</button><button class="gv" onclick="marca('{rid}')">Marcar como gravado</button></div></div>""")
    n = len(blocos)
    minutos = f"{total // 60} min {total % 60:02d} s" if total >= 60 else f"{total} s"
    doc = f"""<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Dia de gravação</title><style>{CSS}</style></head><body><div class="wrap"><h1>Dia de gravação</h1>
<p class="sub">{n} {'roteiro' if n == 1 else 'roteiros'}, cerca de {minutos} de fala no total (estimativa a 150 palavras por minuto). Gerado em {date.today().strftime('%d/%m/%Y')}. <span id="conta"></span></p>
{''.join(blocos) or '<p class="sub">Nenhum roteiro com fala nesse estado. Aprove um roteiro ou rode com --estado todos.</p>'}</div>
<div id="tp"><div class="guia"></div><div class="txt"></div><div class="barra"><button onclick="joga()">Play / pausa (espaço)</button>
<button onclick="velo(-5)">Mais devagar</button><button onclick="velo(5)">Mais rápido</button><button onclick="letra(-4)">A-</button><button onclick="letra(4)">A+</button>
<button onclick="espelha()">Espelhar</button><button onclick="volta()">Do começo</button><button onclick="fecha()">Fechar (Esc)</button><span class="st"></span></div></div>
<script>{JS}</script></body></html>"""
    saida = a.saida or os.path.join(pasta, "gravacao.html")
    open(saida, "w", encoding="utf-8").write(doc)
    print(f"Dia de gravação: {saida}  ({n} {'roteiro' if n == 1 else 'roteiros'}, cerca de {minutos} de fala)")


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    main()
