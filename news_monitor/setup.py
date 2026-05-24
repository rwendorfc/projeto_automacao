"""Script de instalação e configuração inicial do sistema."""

import subprocess
import sys
import os


DEPENDENCIAS = [
    "anthropic>=0.40.0",
    "beautifulsoup4>=4.12.0",
    "lxml>=5.0.0",
    "pandas>=2.0.0",
    "requests>=2.28.0",
    "typing_extensions>=4.0.0",
    "pydantic>=2.0.0",
    "httpx>=0.24.0",
]


def instalar():
    print("Instalando dependências...")
    subprocess.check_call([sys.executable, "-m", "pip", "install"] + DEPENDENCIAS)
    print("\nDependências instaladas com sucesso!")


def verificar_chaves():
    print("\n--- Configuração de Chaves ---")

    api_key = os.environ.get("ANTHROPIC_API_KEY", "")
    if api_key:
        print(f"✅ ANTHROPIC_API_KEY definida ({api_key[:8]}...)")
    else:
        print("⚠️  ANTHROPIC_API_KEY não definida.")
        print("   Configure com: export ANTHROPIC_API_KEY='sk-ant-...'")
        print("   Obtenha em: https://console.anthropic.com/")

    newsapi_key = os.environ.get("NEWSAPI_KEY", "")
    if newsapi_key:
        print(f"✅ NEWSAPI_KEY definida")
    else:
        print("ℹ️  NEWSAPI_KEY não definida (opcional).")
        print("   Configure com: export NEWSAPI_KEY='sua-chave'")
        print("   Obtenha gratuitamente em: https://newsapi.org/register")


def testar():
    print("\n--- Teste de Importações ---")
    try:
        from news_fetcher import buscar_noticias, Noticia
        from sentiment_analyzer import analisar_sentimento, resumo_agregado
        from report_generator import gerar_html, gerar_json
        from config import PESSOAS_MONITORADAS
        print(f"✅ Todos os módulos importados com sucesso!")
        print(f"   Pessoas configuradas: {[p['nome'] for p in PESSOAS_MONITORADAS]}")
    except ImportError as e:
        print(f"❌ Erro de importação: {e}")
        return False
    return True


if __name__ == "__main__":
    instalar()
    verificar_chaves()
    ok = testar()
    if ok:
        print("\n✅ Sistema pronto! Execute:")
        print("   python monitor.py --demo              # teste com dados mockados")
        print("   python monitor.py                     # monitoramento real")
        print("   python monitor.py --ajuda             # ver todas as opções")
