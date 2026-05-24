"""Busca notícias via múltiplas fontes RSS e APIs."""

import time
import logging
import re
import urllib.parse
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta, timezone
from dataclasses import dataclass, field
from email.utils import parsedate_to_datetime

import requests
from bs4 import BeautifulSoup

from config import (
    GNEWS_BASE_URL, GNEWS_PARAMS,
    MAX_NOTICIAS_POR_PESSOA, DIAS_RETROATIVOS,
    REQUEST_TIMEOUT, DELAY_ENTRE_REQUISICOES,
    NEWSAPI_KEY,
)

logger = logging.getLogger(__name__)

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept": "application/rss+xml, application/xml, text/xml, */*",
    "Accept-Language": "pt-BR,pt;q=0.9,en;q=0.8",
}


@dataclass
class Noticia:
    titulo: str
    url: str
    fonte: str
    publicado_em: datetime
    resumo: str = ""
    conteudo: str = ""
    pessoa: str = ""
    sentimento: str = ""
    score_sentimento: float = 0.0
    justificativa: str = ""
    temas: list = field(default_factory=list)


# ──────────────────────────────────────────────
# Helpers
# ──────────────────────────────────────────────

def _parse_data_rss(date_str: str) -> datetime:
    try:
        return parsedate_to_datetime(date_str).astimezone(timezone.utc)
    except Exception:
        return datetime.now(tz=timezone.utc)


def _strip_html(text: str) -> str:
    if not text:
        return ""
    return BeautifulSoup(text, "lxml").get_text(separator=" ", strip=True)


def _clean_title(titulo: str) -> str:
    """Remove o sufixo '- Fonte' que o Google News adiciona aos títulos."""
    return re.sub(r"\s*-\s*[^-]{3,50}$", "", titulo or "").strip()


def _get(url: str, **kwargs) -> requests.Response | None:
    try:
        resp = requests.get(url, headers=HEADERS, timeout=REQUEST_TIMEOUT, **kwargs)
        resp.raise_for_status()
        return resp
    except Exception as e:
        logger.debug(f"GET falhou {url[:80]}: {e}")
        return None


# ──────────────────────────────────────────────
# Fontes de notícias
# ──────────────────────────────────────────────

def _fetch_google_news_rss(termo: str) -> list[dict]:
    """Busca no Google News RSS."""
    params = dict(GNEWS_PARAMS)
    params["q"] = termo
    url = f"{GNEWS_BASE_URL}?{urllib.parse.urlencode(params)}"

    resp = _get(url)
    if not resp:
        return []

    try:
        root = ET.fromstring(resp.content)
    except ET.ParseError as e:
        logger.warning(f"Erro XML Google News: {e}")
        return []

    itens = []
    channel = root.find("channel")
    if not channel:
        return []

    for item in channel.findall("item"):
        titulo = _clean_title(item.findtext("title", ""))
        link = item.findtext("link", "")
        pub_date = item.findtext("pubDate", "")
        desc = _strip_html(item.findtext("description", ""))
        source = item.find("source")
        fonte = source.text if source is not None else ""

        if link:
            itens.append({
                "titulo": titulo,
                "url": link,
                "publicado": pub_date,
                "resumo": desc,
                "fonte": fonte,
            })
    return itens


def _fetch_newsapi(termo: str) -> list[dict]:
    """Busca via NewsAPI.org (requer NEWSAPI_KEY)."""
    if not NEWSAPI_KEY:
        return []

    url = "https://newsapi.org/v2/everything"
    params = {
        "q": f'"{termo}"',
        "language": "pt",
        "sortBy": "publishedAt",
        "pageSize": MAX_NOTICIAS_POR_PESSOA,
        "apiKey": NEWSAPI_KEY,
    }
    resp = _get(url, params=params)
    if not resp:
        return []

    data = resp.json()
    itens = []
    for art in data.get("articles", []):
        itens.append({
            "titulo": art.get("title", ""),
            "url": art.get("url", ""),
            "publicado": art.get("publishedAt", ""),
            "resumo": art.get("description", "") or art.get("content", "")[:300],
            "fonte": art.get("source", {}).get("name", ""),
        })
    return itens


def _parse_newsapi_date(date_str: str) -> datetime:
    """Parseia data ISO do NewsAPI."""
    try:
        return datetime.fromisoformat(date_str.replace("Z", "+00:00"))
    except Exception:
        return datetime.now(tz=timezone.utc)


def _extrair_conteudo(url: str) -> str:
    """Tenta extrair o texto principal de uma URL de notícia."""
    resp = _get(url, allow_redirects=True)
    if not resp:
        return ""

    soup = BeautifulSoup(resp.text, "lxml")
    for tag in soup(["script", "style", "nav", "footer", "header", "aside", "form"]):
        tag.decompose()

    for seletor in ["article", '[class*="content"]', '[class*="article"]', "main"]:
        elem = soup.select_one(seletor)
        if elem:
            texto = elem.get_text(separator=" ", strip=True)
            if len(texto) > 200:
                return texto[:3000]

    paragrafos = soup.find_all("p")
    texto = " ".join(p.get_text(strip=True) for p in paragrafos if len(p.get_text(strip=True)) > 50)
    return texto[:3000]


# ──────────────────────────────────────────────
# Busca principal
# ──────────────────────────────────────────────

def buscar_noticias(pessoa: dict) -> list[Noticia]:
    """Busca notícias para uma pessoa usando múltiplas fontes."""
    noticias: dict[str, Noticia] = {}
    limite_data = datetime.now(tz=timezone.utc) - timedelta(days=DIAS_RETROATIVOS)

    for termo in pessoa["termos_busca"]:
        # Tenta Google News RSS primeiro
        itens = _fetch_google_news_rss(termo)

        # Fallback para NewsAPI se configurado
        if not itens and NEWSAPI_KEY:
            logger.info(f"Fallback para NewsAPI: '{termo}'")
            itens = _fetch_newsapi(termo)

        logger.info(f"'{termo}': {len(itens)} itens no RSS")

        for item in itens:
            if len(noticias) >= MAX_NOTICIAS_POR_PESSOA:
                break

            url = item.get("url", "")
            if not url or url in noticias:
                continue

            # Parseia data dependendo da fonte
            pub_str = item.get("publicado", "")
            if "T" in pub_str:  # formato ISO (NewsAPI)
                publicado = _parse_newsapi_date(pub_str)
            else:  # RFC 2822 (RSS)
                publicado = _parse_data_rss(pub_str)

            if publicado < limite_data:
                continue

            noticias[url] = Noticia(
                titulo=item.get("titulo") or "Sem título",
                url=url,
                fonte=item.get("fonte") or "Desconhecida",
                publicado_em=publicado,
                resumo=(item.get("resumo") or "")[:500],
                pessoa=pessoa["nome"],
            )

        time.sleep(DELAY_ENTRE_REQUISICOES)

    lista = list(noticias.values())[:MAX_NOTICIAS_POR_PESSOA]

    # Enriquece com conteúdo completo (primeiras 5)
    for i, noticia in enumerate(lista[:5]):
        logger.info(f"Extraindo conteúdo ({i+1}/5): {noticia.titulo[:55]}...")
        noticia.conteudo = _extrair_conteudo(noticia.url)
        time.sleep(DELAY_ENTRE_REQUISICOES)

    logger.info(f"Notícias para {pessoa['nome']}: {len(lista)}")
    return lista
