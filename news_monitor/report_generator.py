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
      grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
      gap: 1.5rem;
      margin-bottom: 3rem;
    }}
    .card-resumo {{
      background: white;
      border-radius: 12px;
      padding: 1.5rem;
      box-shadow: 0 2px 8px rgba(0,0,0,0.08);
      border-left: 5px solid #4299e1;
    }}
    .card-resumo h2 {{ font-size: 1.05rem; font-weight: 600; margin-bottom: 0.3rem; }}
    .card-resumo .cargo {{ font-size: 0.8rem; color: #718096; margin-bottom: 0.8rem; }}
    .card-resumo .total {{
      font-size: 2rem; font-weight: 700; color: #2b6cb0;
      line-height: 1;
    }}
    .card-resumo .total-label {{ font-size: 0.72rem; color: #a0aec0; text-transform: uppercase; margin-top: 2px; }}

    .secao-pessoa {{ margin-bottom: 3rem; }}
    .secao-pessoa h2 {{
      font-size: 1.3rem; font-weight: 700;
      border-bottom: 2px solid #e2e8f0;
      padding-bottom: 0.5rem; margin-bottom: 1.5rem; color: #2d3748;
    }}
    .noticias-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(360px, 1fr));
      gap: 1rem;
    }}
    .card-noticia {{
      background: white; border-radius: 10px; padding: 1.2rem;
      box-shadow: 0 1px 4px rgba(0,0,0,0.08);
      border-top: 3px solid #4299e1;
    }}
    .noticia-titulo {{ font-size: 0.9rem; font-weight: 600; line-height: 1.4; margin-bottom: 0.4rem; }}
    .noticia-titulo a {{ color: #2b6cb0; text-decoration: none; }}
    .noticia-titulo a:hover {{ text-decoration: underline; }}
    .noticia-meta {{ font-size: 0.72rem; color: #a0aec0; margin-bottom: 0.5rem; }}
    .noticia-resumo {{ font-size: 0.82rem; color: #4a5568; line-height: 1.5; }}

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
  <p>Gerado em {data_geracao} | Período: últimos {dias} dias</p>
</header>
<div class="container">
  <h2 style="margin-bottom:1rem;color:#2d3748;">Resumo Executivo</h2>
  <div class="resumo-grid">
    {cards_resumo}
  </div>

  <h2 style="margin-bottom:1.5rem;color:#2d3748;">Notícias por Pessoa</h2>
  {secoes_noticias}
</div>
<footer>Sistema de Monitoramento de Notícias · {data_geracao}</footer>
</body>
</html>"""


def _card_resumo(pessoa_nome: str, cargo: str, total: int) -> str:
    return f"""
    <div class="card-resumo">
      <h2>{pessoa_nome}</h2>
      <div class="cargo">{cargo}</div>
      <div class="total">{total}</div>
      <div class="total-label">notícia(s)</div>
    </div>"""


def _card_noticia(noticia) -> str:
    data_str = noticia.publicado_em.strftime("%d/%m/%Y %H:%M")
    resumo = noticia.resumo[:200] + "..." if len(noticia.resumo) > 200 else noticia.resumo
    return f"""
    <div class="card-noticia">
      <div class="noticia-titulo">
        <a href="{noticia.url}" target="_blank" rel="noopener">{noticia.titulo}</a>
      </div>
      <div class="noticia-meta">{noticia.fonte} · {data_str}</div>
      <div class="noticia-resumo">{resumo}</div>
    </div>"""


def gerar_html(resultados: list, output_dir: str) -> str:
    data_str = datetime.now(tz=timezone.utc).strftime("%d/%m/%Y %H:%M UTC")

    cards_resumo_html = ""
    secoes_html = ""

    for item in resultados:
        pessoa = item["pessoa"]
        noticias = item["noticias"]

        cards_resumo_html += _card_resumo(pessoa["nome"], pessoa["cargo"], len(noticias))

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
    os.makedirs(output_dir, exist_ok=True)
    dados = []
    for item in resultados:
        noticias_json = [
            {
                "titulo": n.titulo,
                "url": n.url,
                "fonte": n.fonte,
                "publicado_em": n.publicado_em.isoformat(),
                "resumo": n.resumo,
            }
            for n in item["noticias"]
        ]
        dados.append({
            "pessoa": item["pessoa"]["nome"],
            "cargo": item["pessoa"]["cargo"],
            "total_noticias": len(item["noticias"]),
            "noticias": noticias_json,
        })

    caminho = os.path.join(output_dir, "resultados.json")
    with open(caminho, "w", encoding="utf-8") as f:
        json.dump({"gerado_em": datetime.now(tz=timezone.utc).isoformat(), "dados": dados}, f, ensure_ascii=False, indent=2)
    return caminho
