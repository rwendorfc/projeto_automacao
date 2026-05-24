"""
Sistema de Monitoramento de Notícias com Análise de Sentimento.

Uso:
  python monitor.py                          # executa monitoramento completo
  python monitor.py --demo                   # modo demonstração com dados mockados
  python monitor.py --sem-sentimento         # coleta notícias sem análise de sentimento
  python monitor.py --pessoa "Ronaldo Caiado"  # monitora apenas uma pessoa
  python monitor.py --saida /caminho/saida   # define diretório de saída

Variáveis de ambiente:
  ANTHROPIC_API_KEY  — necessária para análise de sentimento via Claude
  NEWSAPI_KEY        — opcional, aumenta cobertura de notícias (newsapi.org)
"""

import argparse
import logging
import os
import sys
import time

from config import PESSOAS_MONITORADAS, OUTPUT_DIR, DELAY_ENTRE_REQUISICOES, ANTHROPIC_API_KEY
from news_fetcher import buscar_noticias
from sentiment_analyzer import analisar_sentimento, resumo_agregado
from report_generator import gerar_html, gerar_json

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger(__name__)

SENTIMENTO_EMOJI = {
    "Positivo": "✅",
    "Negativo": "❌",
    "Neutro": "⬜",
    "Misto": "🔶",
}


def executar(pessoas: list, analisar: bool = True, demo: bool = False) -> list:
    """Executa o monitoramento completo para a lista de pessoas."""
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

        if analisar and noticias and not demo:
            if not ANTHROPIC_API_KEY:
                logger.warning("ANTHROPIC_API_KEY não definida — pulando análise de sentimento.")
                analisar = False
            else:
                logger.info(f"Analisando sentimento de {len(noticias)} notícias via Claude...")
                for noticia in noticias:
                    resultado = analisar_sentimento(noticia)
                    noticia.sentimento = resultado.get("sentimento", "Neutro")
                    noticia.score_sentimento = float(resultado.get("score", 0.0))
                    noticia.justificativa = resultado.get("justificativa", "")
                    noticia.temas = resultado.get("temas", [])
                    time.sleep(0.3)

        # No modo demo o sentimento já vem pré-preenchido
        resumo = resumo_agregado(noticias) if noticias else {}
        resultados.append({"pessoa": pessoa, "noticias": noticias, "resumo": resumo})

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
        resumo = item["resumo"]
        n = len(item["noticias"])

        if resumo:
            tom = resumo.get("tom_geral", "Neutro")
            score = resumo.get("score_medio", 0.0)
            emoji = SENTIMENTO_EMOJI.get(tom, "")
            dist = resumo.get("distribuicao", {})

            print(f"\n{emoji} {nome}")
            print(f"   {cargo}")
            print(f"   Tom: {tom:<10} Score: {score:+.2f}  ({n} notícias)")
            print(f"   Pos: {dist.get('Positivo',0)}  Neg: {dist.get('Negativo',0)}  "
                  f"Neu: {dist.get('Neutro',0)}  Mis: {dist.get('Misto',0)}")
            if resumo.get("top_temas"):
                print(f"   Temas: {', '.join(resumo['top_temas'])}")
        else:
            print(f"\n○ {nome}: sem notícias no período")

    print("\n" + "=" * largura)


def main():
    parser = argparse.ArgumentParser(
        description="Monitoramento de notícias com análise de sentimento",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument("--demo", action="store_true",
                        help="Modo demonstração com dados mockados (não requer rede)")
    parser.add_argument("--sem-sentimento", action="store_true",
                        help="Não executa análise de sentimento")
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
    if not args.demo and not ANTHROPIC_API_KEY and not args.sem_sentimento:
        logger.warning("ANTHROPIC_API_KEY não definida. Análise de sentimento será pulada.")
        logger.warning("Configure: export ANTHROPIC_API_KEY='sua-chave-aqui'")

    resultados = executar(pessoas, analisar=not args.sem_sentimento, demo=args.demo)

    caminho_html = gerar_html(resultados, args.saida)
    caminho_json = gerar_json(resultados, args.saida)

    imprimir_resumo_terminal(resultados)

    print(f"\nRelatório HTML → {caminho_html}")
    print(f"Dados JSON     → {caminho_json}")


if __name__ == "__main__":
    main()
