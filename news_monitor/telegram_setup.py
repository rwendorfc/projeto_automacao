"""
Script de configuração e teste do Telegram.

Uso:
  python telegram_setup.py

Siga as instruções na tela.
"""

import os
import sys
import requests

def verificar_token(token: str) -> bool:
    resp = requests.get(f"https://api.telegram.org/bot{token}/getMe", timeout=10)
    if resp.ok:
        nome = resp.json()["result"].get("first_name", "")
        username = resp.json()["result"].get("username", "")
        print(f"  Bot válido: {nome} (@{username})")
        return True
    print(f"  Token inválido: {resp.text[:100]}")
    return False


def buscar_chat_id(token: str) -> str:
    resp = requests.get(f"https://api.telegram.org/bot{token}/getUpdates", timeout=10)
    if not resp.ok:
        return ""
    updates = resp.json().get("result", [])
    if not updates:
        return ""
    ultimo = updates[-1]
    chat = ultimo.get("message", {}).get("chat", {})
    return str(chat.get("id", ""))


def enviar_teste(token: str, chat_id: str) -> bool:
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    resp = requests.post(url, json={
        "chat_id": chat_id,
        "text": "✅ *Monitor de Notícias configurado com sucesso!*\n\nVocê receberá os resumos de notícias aqui a cada 4 horas.",
        "parse_mode": "Markdown",
    }, timeout=10)
    return resp.ok


def salvar_env(token: str, chat_id: str):
    env_path = os.path.join(os.path.dirname(__file__), "..", ".env")
    env_path = os.path.abspath(env_path)

    linhas = []
    if os.path.exists(env_path):
        with open(env_path) as f:
            linhas = f.readlines()

    # Remove linhas antigas de telegram
    linhas = [l for l in linhas if not l.startswith("TELEGRAM_")]

    # Adiciona as novas
    linhas += [
        f"TELEGRAM_BOT_TOKEN={token}\n",
        f"TELEGRAM_CHAT_ID={chat_id}\n",
    ]

    with open(env_path, "w") as f:
        f.writelines(linhas)
    print(f"  Salvo em: {env_path}")


def main():
    print("=" * 50)
    print(" CONFIGURAÇÃO DO TELEGRAM BOT")
    print("=" * 50)

    # Token
    token = os.environ.get("TELEGRAM_BOT_TOKEN", "").strip()
    if not token:
        print("\nCole o token do seu bot (obtido no @BotFather):")
        token = input("Token: ").strip()

    if not token:
        print("Token não informado. Abortando.")
        sys.exit(1)

    print("\n1. Verificando token...")
    if not verificar_token(token):
        sys.exit(1)

    # chat_id
    print("\n2. Buscando chat_id...")
    chat_id = buscar_chat_id(token)

    if not chat_id:
        print("\n  Nenhuma mensagem encontrada.")
        print("  >> Abra o Telegram, procure pelo seu bot e envie qualquer mensagem (ex: 'oi')")
        input("  Pressione ENTER depois de enviar a mensagem...")
        chat_id = buscar_chat_id(token)

    if not chat_id:
        print("  Ainda sem mensagem recebida. Tente novamente.")
        sys.exit(1)

    print(f"  chat_id encontrado: {chat_id}")

    # Envia mensagem de teste
    print("\n3. Enviando mensagem de teste...")
    if enviar_teste(token, chat_id):
        print("  Mensagem enviada! Verifique o Telegram.")
    else:
        print("  Falha ao enviar. Verifique o token e chat_id.")
        sys.exit(1)

    # Salva no .env
    print("\n4. Salvando configuração no .env...")
    salvar_env(token, chat_id)

    print("\n" + "=" * 50)
    print(" CONFIGURAÇÃO CONCLUÍDA!")
    print("=" * 50)
    print("\nCarregue as variáveis e teste:")
    print("  export $(grep -v '^#' ../.env | xargs)")
    print("  python monitor.py --demo --telegram")


if __name__ == "__main__":
    main()
