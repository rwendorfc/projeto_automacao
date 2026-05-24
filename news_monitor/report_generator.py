"""Geração de relatórios HTML e JSON."""

import json
import os
from datetime import datetime, timezone

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Monitoramento de Notícias — {data_geracao}</title>
  <style>
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{ font-family: 'Segoe UI', system-ui, sans-serif; background: #f0f4f8; color: #1a202c; }}
    header {{
      background: linear-gradient(135deg, #1a365d 0%, #2d3748 100%);
      color: white; padding: 2rem;
      box-shadow: 0 4px 6px rgba(0,0,0,0.3);
    }}
    header h1 {{ font-size: 1.8rem; font-weight: 700; }}
    header p {{ opacity: 0.8; margin-top: 0.3rem; font-size: 0.95rem; }}
    .container {{ max-width: 1200px; margin: 0 auto; padding: 2rem 1rem; }}

    .resumo-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
      gap: 1.5rem;
      margin-bottom: 3rem;
    }}
    .card-resumo {{
      background: white;
      border-radius: 12px;
      padding: 1.5rem;
      box-shadow: 0 2px 8px rgba(0,0,0,0.08);
      border-left: 5px solid #ccc;
    }}
    .card-resumo.positivo {{ border-left-color: #38a169; }}
    .card-resumo.negativo {{ border-left-color: #e53e3e; }}
    .card-resumo.neutro  {{ border-left-color: #718096; }}
    .card-resumo.misto   {{ border-left-color: #d69e2e; }}

    .card-resumo h2 {{ font-size: 1.1rem; font-weight: 600; margin-bottom: 0.3rem; }}
    .card-resumo .cargo {{ font-size: 0.8rem; color: #718096; margin-bottom: 1rem; }}
    .badge {{
      display: inline-block;
      padding: 0.25rem 0.75rem;
      border-radius: 999px;
      font-size: 0.78rem;
      font-weight: 600;
      margin-bottom: 0.8rem;
    }}
    .badge.Positivo {{ background: #c6f6d5; color: #276749; }}
    .badge.Negativo {{ background: #fed7d7; color: #9b2c2c; }}
    .badge.Neutro   {{ background: #e2e8f0; color: #4a5568; }}
    .badge.Misto    {{ background: #fefcbf; color: #744210; }}

    .score-bar-wrap {{ margin: 0.5rem 0; }}
    .score-label {{ font-size: 0.75rem; color: #718096; margin-bottom: 2px; }}
    .score-bar {{ height: 8px; background: #e2e8f0; border-radius: 4px; overflow: hidden; }}
    .score-fill {{ height: 100%; border-radius: 4px; transition: width 0.3s; }}
    .score-fill.pos {{ background: #38a169; }}
    .score-fill.neg {{ background: #e53e3e; }}
    .score-fill.neu {{ background: #a0aec0; }}

    .stats {{ display: flex; gap: 1rem; flex-wrap: wrap; margin: 0.8rem 0; }}
    .stat {{ text-align: center; }}
    .stat .num {{ font-size: 1.3rem; font-weight: 700; }}
    .stat .lbl {{ font-size: 0.7rem; color: #718096; text-transform: uppercase; }}

    .temas {{ margin-top: 0.8rem; }}
    .tema-tag {{
      display: inline-block;
      background: #ebf4ff;
      color: #2b6cb0;
      border-radius: 4px;
      padding: 2px 8px;
      font-size: 0.72rem;
      margin: 2px;
    }}

    .secao-pessoa {{ margin-bottom: 3rem; }}
    .secao-pessoa h2 {{
      font-size: 1.3rem;
      font-weight: 700;
      border-bottom: 2px solid #e2e8f0;
      padding-bottom: 0.5rem;
      margin-bottom: 1.5rem;
      color: #2d3748;
    }}
    .noticias-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(360px, 1fr));
      gap: 1rem;
    }}
    .card-noticia {{
      background: white;
      border-radius: 10px;
      padding: 1.2rem;
      box-shadow: 0 1px 4px rgba(0,0,0,0.08);
      border-top: 3px solid #e2e8f0;
    }}
    .card-noticia.Positivo {{ border-top-color: #38a169; }}
    .card-noticia.Negativo {{ border-top-color: #e53e3e; }}
    .card-noticia.Neutro   {{ border-top-color: #a0aec0; }}
    .card-noticia.Misto    {{ border-top-color: #d69e2e; }}

    .noticia-header {{ display: flex; justify-content: space-between; align-items: flex-start; gap: 0.5rem; margin-bottom: 0.6rem; }}
    .noticia-titulo {{ font-size: 0.9rem; font-weight: 600; line-height: 1.4; flex: 1; }}
    .noticia-titulo a {{ color: #2b6cb0; text-decoration: none; }}
    .noticia-titulo a:hover {{ text-decoration: underline; }}
    .noticia-meta {{ font-size: 0.72rem; color: #a0aec0; margin-bottom: 0.5rem; }}
    .noticia-resumo {{ font-size: 0.82rem; color: #4a5568; line-height: 1.5; margin-bottom: 0.6rem; }}
    .noticia-justificativa {{ font-size: 0.78rem; color: #718096; font-style: italic; border-left: 3px solid #e2e8f0; padding-left: 0.5rem; }}
    .relevancia {{ font-size: 0.7rem; color: #718096; margin-top: 0.5rem; }}

    footer {{ text-align: center; color: #a0aec0; font-size: 0.78rem; padding: 2rem; }}

    @media (max-width: 600px) {{
      .noticias-grid {{ grid-template-columns: 1fr; }}
      .resumo-grid {{ grid-template-columns: 1fr; }}
    }}
  </style>
</head>
<body>
<header>
  <h1>Monitoramento de Notícias</h1>
  <p>Análise de sentimento — Gerado em {data_geracao} | Período: últimos {dias} dias</p>
</header>
<div class="container">
  <h2 style="margin-bottom:1rem;color:#2d3748;">Resumo Executivo</h2>
  <div class="resumo-grid">
    {cards_resumo}
  </div>

  <h2 style="margin-bottom:1.5rem;color:#2d3748;">Notícias por Pessoa</h2>
  {secoes_noticias}
</div>
<footer>Sistema de Monitoramento de Notícias com Análise de Sentimento · {data_geracao}</footer>
</body>
</html>"""


def _cor_classe(tom: str) -> str:
    return tom.lower() if tom in ("Positivo", "Negativo", "Neutro", "Misto") else "neutro"


def _score_bar(score: float) -> str:
    pct = int((score + 1) / 2 * 100)
    classe = "pos" if score > 0.1 else ("neg" if score < -0.1 else "neu")
    return f"""
    <div class="score-bar-wrap">
      <div class="score-label">Score: {score:+.2f}</div>
      <div class="score-bar"><div class="score-fill {classe}" style="width:{pct}%"></div></div>
    </div>"""


def _card_resumo(pessoa_nome: str, cargo: str, resumo: dict) -> str:
    if not resumo:
        return ""
    tom = resumo.get("tom_geral", "Neutro")
    dist = resumo.get("distribuicao", {})
    temas_html = "".join(f'<span class="tema-tag">{t}</span>' for t in resumo.get("top_temas", []))
    return f"""
    <div class="card-resumo {tom.lower()}">
      <h2>{pessoa_nome}</h2>
      <div class="cargo">{cargo}</div>
      <span class="badge {tom}">{tom}</span>
      {_score_bar(resumo.get('score_medio', 0))}
      <div class="stats">
        <div class="stat"><div class="num">{resumo.get('total_noticias', 0)}</div><div class="lbl">Notícias</div></div>
        <div class="stat"><div class="num" style="color:#38a169">{dist.get('Positivo',0)}</div><div class="lbl">Positivas</div></div>
        <div class="stat"><div class="num" style="color:#e53e3e">{dist.get('Negativo',0)}</div><div class="lbl">Negativas</div></div>
        <div class="stat"><div class="num" style="color:#718096">{dist.get('Neutro',0)}</div><div class="lbl">Neutras</div></div>
      </div>
      <div class="temas">{temas_html}</div>
    </div>"""


def _card_noticia(noticia) -> str:
    data_str = noticia.publicado_em.strftime("%d/%m/%Y %H:%M")
    resumo = noticia.resumo[:200] + "..." if len(noticia.resumo) > 200 else noticia.resumo
    temas_html = "".join(f'<span class="tema-tag">{t}</span>' for t in noticia.temas)
    return f"""
    <div class="card-noticia {noticia.sentimento}">
      <div class="noticia-header">
        <div class="noticia-titulo">
          <a href="{noticia.url}" target="_blank" rel="noopener">{noticia.titulo}</a>
        </div>
        <span class="badge {noticia.sentimento}" style="white-space:nowrap">{noticia.sentimento}</span>
      </div>
      <div class="noticia-meta">{noticia.fonte} · {data_str}</div>
      <div class="noticia-resumo">{resumo}</div>
      {f'<div class="noticia-justificativa">{noticia.justificativa}</div>' if noticia.justificativa else ''}
      <div style="margin-top:0.5rem">{temas_html}</div>
      <div class="relevancia">Score: {noticia.score_sentimento:+.2f}</div>
    </div>"""


def gerar_html(resultados: list, output_dir: str) -> str:
    data_str = datetime.now(tz=timezone.utc).strftime("%d/%m/%Y %H:%M UTC")

    cards_resumo_html = ""
    secoes_html = ""

    for item in resultados:
        pessoa = item["pessoa"]
        noticias = item["noticias"]
        resumo = item["resumo"]

        cards_resumo_html += _card_resumo(pessoa["nome"], pessoa["cargo"], resumo)

        if noticias:
            cards_noticias = "".join(_card_noticia(n) for n in noticias)
            secoes_html += f"""
            <div class="secao-pessoa">
              <h2>{pessoa['nome']} <small style="font-size:0.7em;color:#718096;font-weight:400">({pessoa['cargo']})</small></h2>
              <div class="noticias-grid">{cards_noticias}</div>
            </div>"""
        else:
            secoes_html += f"""
            <div class="secao-pessoa">
              <h2>{pessoa['nome']}</h2>
              <p style="color:#a0aec0;font-style:italic">Nenhuma notícia encontrada no período.</p>
            </div>"""

    html = HTML_TEMPLATE.format(
        data_geracao=data_str,
        dias=7,
        cards_resumo=cards_resumo_html,
        secoes_noticias=secoes_html,
    )

    os.makedirs(output_dir, exist_ok=True)
    caminho = os.path.join(output_dir, "relatorio.html")
    with open(caminho, "w", encoding="utf-8") as f:
        f.write(html)
    return caminho


def gerar_json(resultados: list, output_dir: str) -> str:
    """Salva os resultados em JSON estruturado."""
    os.makedirs(output_dir, exist_ok=True)
    dados = []
    for item in resultados:
        noticias_json = []
        for n in item["noticias"]:
            noticias_json.append({
                "titulo": n.titulo,
                "url": n.url,
                "fonte": n.fonte,
                "publicado_em": n.publicado_em.isoformat(),
                "resumo": n.resumo,
                "sentimento": n.sentimento,
                "score_sentimento": n.score_sentimento,
                "justificativa": n.justificativa,
                "temas": n.temas,
            })
        dados.append({
            "pessoa": item["pessoa"]["nome"],
            "cargo": item["pessoa"]["cargo"],
            "resumo": item["resumo"],
            "noticias": noticias_json,
        })

    caminho = os.path.join(output_dir, "resultados.json")
    with open(caminho, "w", encoding="utf-8") as f:
        json.dump({"gerado_em": datetime.now(tz=timezone.utc).isoformat(), "dados": dados}, f, ensure_ascii=False, indent=2)
    return caminho
