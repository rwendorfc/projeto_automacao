"""Configurações do sistema de monitoramento de notícias."""

PESSOAS_MONITORADAS = [
    {
        "nome": "Gracinha Caiado",
        "termos_busca": ["Gracinha Caiado", "Ana Carolina Caiado"],
        "cargo": "Primeira-dama de Goiás",
    },
    {
        "nome": "Ronaldo Caiado",
        "termos_busca": ["Ronaldo Caiado", "Caiado governador"],
        "cargo": "Governador de Goiás",
    },
    {
        "nome": "Adryanna Caiado",
        "termos_busca": ["Adryanna Caiado"],
        "cargo": "Família Caiado",
    },
    {
        "nome": "Roberta Wendorf Carvalho",
        "termos_busca": ["Roberta Wendorf", "Roberta Wendorf Carvalho"],
        "cargo": "Personalidade pública",
    },
    {
        "nome": "Decio Wendorf",
        "termos_busca": ["Decio Wendorf", "Décio Wendorf"],
        "cargo": "Personalidade pública",
    },
    {
        "nome": "Daniel Vilela",
        "termos_busca": ["Daniel Vilela", "Daniel Vilela Goiás"],
        "cargo": "Político de Goiás",
    },
    {
        "nome": "Iara Netto Vilela",
        "termos_busca": ["Iara Netto Vilela", "Iara Vilela"],
        "cargo": "Personalidade pública",
    },
]

# Google News RSS
GNEWS_BASE_URL = "https://news.google.com/rss/search"
GNEWS_PARAMS = {
    "hl": "pt-BR",
    "gl": "BR",
    "ceid": "BR:pt-419",
}

MAX_NOTICIAS_POR_PESSOA = 10
DIAS_RETROATIVOS = 7
REQUEST_TIMEOUT = 15
DELAY_ENTRE_REQUISICOES = 1.5  # segundos

OUTPUT_DIR = "resultados"

# Agendamento
INTERVALO_HORAS = 4
# Horários fixos de execução (alternativa ao intervalo); deixe vazio para usar INTERVALO_HORAS
# Exemplo: ["06:00", "10:00", "14:00", "18:00", "22:00"]
HORARIOS_FIXOS: list[str] = []

# Chaves de API (configure via variáveis de ambiente ou arquivo .env)
import os
NEWSAPI_KEY = os.environ.get("NEWSAPI_KEY", "")  # https://newsapi.org (plano gratuito disponível)

# WhatsApp — CallMeBot (gratuito): https://www.callmebot.com/blog/free-api-whatsapp-messages/
# Ativação: salve +34 644 59 67 47 como "CallMeBot" e envie "I allow callmebot to send me messages"
WHATSAPP_PHONE = os.environ.get("WHATSAPP_PHONE", "")      # ex: +5571996697450
CALLMEBOT_API_KEY = os.environ.get("CALLMEBOT_API_KEY", "") # chave enviada pelo CallMeBot após ativação
