"""Envio de notificações via WhatsApp usando a API gratuita CallMeBot."""

import logging
import urllib.parse
import requests

from config import WHATSAPP_PHONE, CALLMEBOT_API_KEY

logger = logging.getLogger(__name__)

CALLMEBOT_URL = "https://api.callmebot.com/whatsapp.php"


def _esta_configurado() -> bool:
    return bool(WHATSAPP_PHONE and CALLMEBOT_API_KEY)


def enviar(mensagem: str) -> bool:
    """Envia mensagem de texto via WhatsApp. Retorna True se enviou com sucesso."""
    if not _esta_configurado():
        logger.warning("WhatsApp não configurado — defina WHATSAPP_PHONE e CALLMEBOT_API_KEY.")
        return False

    params = {
        "phone": WHATSAPP_PHONE,
        "text": mensagem,
        "apikey": CALLMEBOT_API_KEY,
    }
    try:
        url = f"{CALLMEBOT_URL}?{urllib.parse.urlencode(params)}"
        resp = requests.get(url, timeout=15)
        if resp.ok:
            logger.info(f"WhatsApp enviado para {WHATSAPP_PHONE}")
            return True
        else:
            logger.warning(f"Falha no envio WhatsApp: {resp.status_code} — {resp.text[:100]}")
            return False
    except Exception as e:
        logger.error(f"Erro ao enviar WhatsApp: {e}")
        return False


def montar_resumo(resultados: list, data_str: str = "") -> str:
    """Monta a mensagem de resumo do monitoramento para WhatsApp."""
    from datetime import datetime
    if not data_str:
        data_str = datetime.now().strftime("%d/%m/%Y %H:%M")

    linhas = [
        f"🗞 *Monitor de Notícias*",
        f"📅 {data_str}",
        "─────────────────────",
    ]

    total = 0
    for item in resultados:
        nome = item["pessoa"]["nome"].split()[0] + " " + item["pessoa"]["nome"].split()[-1]
        n = len(item["noticias"])
        total += n
        marcador = "●" if n else "○"
        linhas.append(f"{marcador} {nome}: {n} notícia(s)")
        # Adiciona os 2 primeiros títulos como sub-itens
        for noticia in item["noticias"][:2]:
            titulo = noticia.titulo[:60] + ("…" if len(noticia.titulo) > 60 else "")
            linhas.append(f"  · {titulo}")

    linhas += [
        "─────────────────────",
        f"📊 Total: *{total} notícias*",
    ]

    return "\n".join(linhas)
