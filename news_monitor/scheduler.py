"""
Daemon de agendamento do monitoramento de notícias.

Executa o monitoramento a cada 4 horas (configurável em config.py).
Cada execução gera resultados em resultados/YYYY-MM-DD_HH-MM/ para
manter histórico completo.

Uso:
  python scheduler.py            # inicia daemon (roda indefinidamente)
  python scheduler.py --uma-vez  # executa uma vez imediatamente e sai
  python scheduler.py --status   # mostra próxima execução agendada
"""

import argparse
import logging
import os
import shutil
import signal
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import schedule

# Garante que o diretório do módulo está no path
sys.path.insert(0, str(Path(__file__).parent))

from config import INTERVALO_HORAS, HORARIOS_FIXOS, OUTPUT_DIR

LOG_DIR = Path(__file__).parent / "logs"
LOG_DIR.mkdir(exist_ok=True)
LOG_FILE = LOG_DIR / "scheduler.log"

_fmt = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
_root = logging.getLogger()
_root.setLevel(logging.INFO)
_root.addHandler(logging.StreamHandler(sys.stdout))
_root.handlers[-1].setFormatter(_fmt)
_fh = logging.FileHandler(LOG_FILE, encoding="utf-8")
_fh.setFormatter(_fmt)
_root.addHandler(_fh)

logger = logging.getLogger(__name__)

_running = True


def _signal_handler(sig, frame):
    global _running
    logger.info(f"Sinal {sig} recebido — encerrando daemon.")
    _running = False


def _output_dir_para_execucao() -> str:
    """Cria um diretório de saída com timestamp para cada execução."""
    agora = datetime.now()
    subdir = agora.strftime("%Y-%m-%d_%H-%M")
    caminho = Path(__file__).parent / OUTPUT_DIR / subdir
    caminho.mkdir(parents=True, exist_ok=True)
    return str(caminho)


def _atualizar_symlink_latest(saida: str) -> None:
    """Mantém um symlink 'latest' apontando para a execução mais recente."""
    base = Path(__file__).parent / OUTPUT_DIR
    latest = base / "latest"
    try:
        if latest.is_symlink() or latest.exists():
            latest.unlink()
        latest.symlink_to(Path(saida).name)
    except Exception as e:
        logger.debug(f"Não foi possível atualizar symlink latest: {e}")


def _limpar_execucoes_antigas(manter: int = 24) -> None:
    """Remove execuções mais antigas, mantendo as últimas `manter`."""
    base = Path(__file__).parent / OUTPUT_DIR
    execucoes = sorted(
        [d for d in base.iterdir() if d.is_dir() and d.name not in ("latest",)],
        key=lambda d: d.name,
    )
    para_remover = execucoes[:-manter] if len(execucoes) > manter else []
    for d in para_remover:
        try:
            shutil.rmtree(d)
            logger.info(f"Execução antiga removida: {d.name}")
        except Exception as e:
            logger.warning(f"Não foi possível remover {d}: {e}")


def executar_monitoramento() -> None:
    """Executa um ciclo completo de monitoramento."""
    inicio = datetime.now()
    logger.info("=" * 60)
    logger.info(f"INICIANDO EXECUÇÃO — {inicio.strftime('%d/%m/%Y %H:%M:%S')}")
    logger.info("=" * 60)

    try:
        from monitor import executar
        from report_generator import gerar_html, gerar_json
        from config import PESSOAS_MONITORADAS

        saida = _output_dir_para_execucao()
        resultados = executar(PESSOAS_MONITORADAS)

        caminho_html = gerar_html(resultados, saida)
        caminho_json = gerar_json(resultados, saida)

        _atualizar_symlink_latest(saida)
        _limpar_execucoes_antigas(manter=24)

        fim = datetime.now()
        duracao = (fim - inicio).total_seconds()

        total_noticias = sum(len(r["noticias"]) for r in resultados)
        logger.info(f"Execução concluída em {duracao:.1f}s — {total_noticias} notícias coletadas")
        logger.info(f"HTML → {caminho_html}")
        logger.info(f"JSON → {caminho_json}")

    except Exception as e:
        logger.error(f"Erro durante execução: {e}", exc_info=True)


def configurar_agenda() -> None:
    """Configura o schedule conforme config.py."""
    schedule.clear()

    if HORARIOS_FIXOS:
        for horario in HORARIOS_FIXOS:
            schedule.every().day.at(horario).do(executar_monitoramento)
            logger.info(f"Agendado: todo dia às {horario}")
    else:
        schedule.every(INTERVALO_HORAS).hours.do(executar_monitoramento)
        logger.info(f"Agendado: a cada {INTERVALO_HORAS} horas")


def proxima_execucao() -> str:
    jobs = schedule.get_jobs()
    if not jobs:
        return "Nenhum job agendado"
    proxima = min(j.next_run for j in jobs)
    return proxima.strftime("%d/%m/%Y %H:%M:%S")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Daemon de agendamento do monitoramento de notícias",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument("--uma-vez", action="store_true",
                        help="Executa uma vez imediatamente e encerra")
    parser.add_argument("--status", action="store_true",
                        help="Mostra configuração e próxima execução")
    args = parser.parse_args()

    if args.uma_vez:
        executar_monitoramento()
        return

    configurar_agenda()

    if args.status:
        print(f"Intervalo configurado : a cada {INTERVALO_HORAS}h")
        if HORARIOS_FIXOS:
            print(f"Horários fixos        : {', '.join(HORARIOS_FIXOS)}")
        print(f"Próxima execução      : {proxima_execucao()}")
        print(f"Log                   : {LOG_FILE}")
        return

    signal.signal(signal.SIGINT, _signal_handler)
    signal.signal(signal.SIGTERM, _signal_handler)

    logger.info(f"Daemon iniciado — intervalo: {INTERVALO_HORAS}h")
    logger.info(f"Próxima execução: {proxima_execucao()}")
    logger.info("Pressione Ctrl+C para encerrar.")

    # Executa imediatamente na inicialização
    logger.info("Executando monitoramento inicial...")
    executar_monitoramento()

    while _running:
        schedule.run_pending()
        time.sleep(30)

    logger.info("Daemon encerrado.")


if __name__ == "__main__":
    main()
