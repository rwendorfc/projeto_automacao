"""Envio de notificações via Telegram Bot API."""

import logging
import requests

from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID

logger = logging.getLogger(__name__)

TELEGRAM_URL = "https://api.telegram.org/bot{token}/sendMessage"


def _esta_configurado() -> bool:
    return bool(TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID)


def enviar(mensagem: str) -> bool:
    """Envia mensagem via Telegram. Retorna True se enviou com sucesso."""
    if not _esta_configurado():
        logger.warning("Telegram não configurado — defina TELEGRAM_BOT_TOKEN e TELEGRAM_CHAT_ID.")
        return False

    url = TELEGRAM_URL.format(token=TELEGRAM_BOT_TOKEN)
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": mensagem,
        "parse_mode": "Markdown",
        "disable_web_page_preview": True,
    }
    try:
        resp = requests.post(url, json=payload, timeout=15)
        if resp.ok:
            logger.info(f"Telegram enviado para chat_id {TELEGRAM_CHAT_ID}")
            return True
        else:
            logger.warning(f"Falha Telegram: {resp.status_code} — {resp.text[:150]}")
            return False
    except Exception as e:
        logger.error(f"Erro ao enviar Telegram: {e}")
        return False


def montar_resumo(resultados: list, data_str: str = "") -> str:
    """Monta a mensagem de resumo para o Telegram (suporta Markdown)."""
    from datetime import datetime
    if not data_str:
        data_str = datetime.now().strftime("%d/%m/%Y %H:%M")

    linhas = [
        "🗞 *Monitor de Notícias*",
        f"📅 {data_str}",
        "─────────────────────",
    ]

    total = 0
    for item in resultados:
        nome = item["pessoa"]["nome"]
        n = len(item["noticias"])
        total += n
        marcador = "●" if n else "○"
        linhas.append(f"{marcador} *{nome}*: {n} notícia(s)")
        for noticia in item["noticias"][:2]:
            titulo = noticia.titulo[:70] + ("…" if len(noticia.titulo) > 70 else "")
            linhas.append(f"  · [{titulo}]({noticia.url})")

    linhas += [
        "─────────────────────",
        f"📊 Total: *{total} notícias coletadas*",
    ]

    return "\n".join(linhas)


def obter_chat_id(token: str) -> str:
    """Utilitário: retorna o chat_id do último usuário que enviou mensagem ao bot."""
    try:
        url = f"https://api.telegram.org/bot{token}/getUpdates"
        resp = requests.get(url, timeout=10)
        data = resp.json()
        updates = data.get("result", [])
        if not updates:
            return ""
        return str(updates[-1]["message"]["chat"]["id"])
    except Exception as e:
        logger.error(f"Erro ao obter chat_id: {e}")
        return ""
