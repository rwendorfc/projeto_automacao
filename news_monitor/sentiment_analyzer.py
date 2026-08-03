"""Análise de sentimento via Claude API."""

import logging
import json
import os

import anthropic

logger = logging.getLogger(__name__)

_client = None


def _get_client() -> anthropic.Anthropic:
    global _client
    if _client is None:
        _client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
    return _client


PROMPT_SENTIMENTO = """Você é um analista de mídia especializado em monitoramento de imagem pública de personalidades brasileiras.

Analise a notícia abaixo sobre {pessoa} e retorne um JSON com a seguinte estrutura:

{{
  "sentimento": "Positivo" | "Negativo" | "Neutro" | "Misto",
  "score": <número de -1.0 a 1.0, onde -1=muito negativo, 0=neutro, 1=muito positivo>,
  "justificativa": "<explicação breve de 1-2 frases sobre o sentimento identificado>",
  "temas": ["<tema1>", "<tema2>"],
  "relevancia": "Alta" | "Média" | "Baixa"
}}

Critérios:
- Positivo: notícia elogiosa, conquistas, resultados positivos, aprovação pública
- Negativo: críticas, escândalos, problemas, denúncias, rejeição
- Neutro: informativo sem tom avaliativo
- Misto: contém elementos positivos e negativos

Notícia:
Título: {titulo}
Fonte: {fonte}
Resumo: {resumo}
{conteudo_extra}

Retorne APENAS o JSON, sem texto adicional."""


def analisar_sentimento(noticia) -> dict:
    """Analisa o sentimento de uma notícia usando Claude."""
    cliente = _get_client()

    conteudo_extra = ""
    if noticia.conteudo:
        conteudo_extra = f"Conteúdo: {noticia.conteudo[:1500]}"

    prompt = PROMPT_SENTIMENTO.format(
        pessoa=noticia.pessoa,
        titulo=noticia.titulo,
        fonte=noticia.fonte,
        resumo=noticia.resumo,
        conteudo_extra=conteudo_extra,
    )

    try:
        resposta = cliente.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=400,
            messages=[{"role": "user", "content": prompt}],
        )
        texto = resposta.content[0].text.strip()

        # Extrai JSON da resposta
        if "```" in texto:
            texto = texto.split("```")[1]
            if texto.startswith("json"):
                texto = texto[4:]

        resultado = json.loads(texto)
        return resultado

    except json.JSONDecodeError as e:
        logger.warning(f"Erro ao parsear JSON do sentimento: {e}")
        return _sentimento_fallback()
    except Exception as e:
        logger.error(f"Erro na análise de sentimento: {e}")
        return _sentimento_fallback()


def _sentimento_fallback() -> dict:
    return {
        "sentimento": "Neutro",
        "score": 0.0,
        "justificativa": "Não foi possível analisar o sentimento.",
        "temas": [],
        "relevancia": "Baixa",
    }


def resumo_agregado(noticias: list) -> dict:
    """Gera um resumo agregado do sentimento para uma pessoa."""
    if not noticias:
        return {}

    scores = [n.score_sentimento for n in noticias]
    score_medio = sum(scores) / len(scores)

    contagem = {"Positivo": 0, "Negativo": 0, "Neutro": 0, "Misto": 0}
    todos_temas = []
    for n in noticias:
        contagem[n.sentimento] = contagem.get(n.sentimento, 0) + 1
        todos_temas.extend(n.temas)

    # Temas mais frequentes
    freq_temas = {}
    for t in todos_temas:
        freq_temas[t] = freq_temas.get(t, 0) + 1
    top_temas = sorted(freq_temas.items(), key=lambda x: x[1], reverse=True)[:5]

    tom_geral = "Neutro"
    if score_medio > 0.2:
        tom_geral = "Positivo"
    elif score_medio < -0.2:
        tom_geral = "Negativo"
    elif any(c > 0 for c in [contagem.get("Positivo", 0), contagem.get("Negativo", 0)]):
        tom_geral = "Misto"

    return {
        "total_noticias": len(noticias),
        "score_medio": round(score_medio, 3),
        "tom_geral": tom_geral,
        "distribuicao": contagem,
        "top_temas": [t[0] for t in top_temas],
    }
