"""
Sistema de Monitoramento de Notícias.

Uso:
  python monitor.py                          # executa monitoramento completo
  python monitor.py --demo                   # modo demonstração com dados mockados
  python monitor.py --pessoa "Ronaldo Caiado"  # monitora apenas uma pessoa
  python monitor.py --saida /caminho/saida   # define diretório de saída

Variáveis de ambiente:
  NEWSAPI_KEY  — opcional, aumenta cobertura de notícias (newsapi.org)
"""

import argparse
import logging
import sys
import time

from config import PESSOAS_MONITORADAS, OUTPUT_DIR, DELAY_ENTRE_REQUISICOES
from news_fetcher import buscar_noticias
from report_generator import gerar_html, gerar_json

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger(__name__)


def executar(pessoas: list, demo: bool = False) -> list:
    """Executa o monitoramento para a lista de pessoas."""
    if demo:
        from demo_data import gerar_noticias_demo
        logger.info("Modo DEMO ativado — usando dados mockados.")

    resultados = []

    for idx, pessoa in enumerate(pessoas, 1):
        logger.info(f"\n[{idx}/{len(pessoas)}] ▶ {pessoa['nome']} ({pessoa['cargo']})")

        if demo:
            from demo_data import gerar_noticias_demo
            noticias = gerar_noticias_demo(pessoa)
        else:
            noticias = buscar_noticias(pessoa)

        resultados.append({"pessoa": pessoa, "noticias": noticias})

        if idx < len(pessoas):
            time.sleep(DELAY_ENTRE_REQUISICOES if not demo else 0)

    return resultados


def imprimir_resumo_terminal(resultados: list) -> None:
    largura = 64
    print("\n" + "=" * largura)
    print(" MONITORAMENTO DE NOTÍCIAS — RESUMO")
    print("=" * largura)

    for item in resultados:
        nome = item["pessoa"]["nome"]
        cargo = item["pessoa"]["cargo"]
        n = len(item["noticias"])

        if n:
            print(f"\n● {nome}")
            print(f"   {cargo}")
            print(f"   {n} notícia(s) encontrada(s)")
            for noticia in item["noticias"][:3]:
                print(f"   · {noticia.titulo[:65]}")
        else:
            print(f"\n○ {nome}: sem notícias no período")

    print("\n" + "=" * largura)


def main():
    parser = argparse.ArgumentParser(
        description="Monitoramento de notícias",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument("--demo", action="store_true",
                        help="Modo demonstração com dados mockados (não requer rede)")
    parser.add_argument("--whatsapp", action="store_true",
                        help="Envia resumo via WhatsApp ao finalizar")
    parser.add_argument("--pessoa", type=str, default=None,
                        help="Nome exato de uma pessoa para monitorar individualmente")
    parser.add_argument("--saida", type=str, default=OUTPUT_DIR,
                        help=f"Diretório de saída (padrão: {OUTPUT_DIR})")
    args = parser.parse_args()

    pessoas = PESSOAS_MONITORADAS
    if args.pessoa:
        pessoas = [p for p in PESSOAS_MONITORADAS if p["nome"].lower() == args.pessoa.lower()]
        if not pessoas:
            nomes = [p["nome"] for p in PESSOAS_MONITORADAS]
            logger.error(f"Pessoa '{args.pessoa}' não encontrada. Disponíveis: {nomes}")
            sys.exit(1)

    logger.info(f"Iniciando monitoramento de {len(pessoas)} pessoa(s)...")

    resultados = executar(pessoas, demo=args.demo)

    caminho_html = gerar_html(resultados, args.saida)
    caminho_json = gerar_json(resultados, args.saida)

    imprimir_resumo_terminal(resultados)

    print(f"\nRelatório HTML → {caminho_html}")
    print(f"Dados JSON     → {caminho_json}")

    if args.whatsapp:
        from whatsapp_notifier import enviar, montar_resumo
        from datetime import datetime
        mensagem = montar_resumo(resultados, datetime.now().strftime("%d/%m/%Y %H:%M"))
        ok = enviar(mensagem)
        if ok:
            print("WhatsApp enviado com sucesso.")
        else:
            print("Falha ao enviar WhatsApp — verifique WHATSAPP_PHONE e CALLMEBOT_API_KEY.")


if __name__ == "__main__":
    main()
