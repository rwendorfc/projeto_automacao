#!/bin/bash
# Wrapper de execução — chamado pelo cron ou manualmente.
# Edite as variáveis abaixo antes de usar.

# ── Configuração ──────────────────────────────────────────────
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ANTHROPIC_API_KEY="${ANTHROPIC_API_KEY:-}"   # ou coloque a chave diretamente aqui
NEWSAPI_KEY="${NEWSAPI_KEY:-}"               # opcional
PYTHON="${PYTHON:-python3}"
LOG_FILE="$SCRIPT_DIR/logs/cron.log"
# ─────────────────────────────────────────────────────────────

mkdir -p "$SCRIPT_DIR/logs"

export ANTHROPIC_API_KEY
export NEWSAPI_KEY

echo "──────────────────────────────────────────────────" >> "$LOG_FILE"
echo "$(date '+%Y-%m-%d %H:%M:%S') Iniciando monitoramento" >> "$LOG_FILE"

cd "$SCRIPT_DIR" && \
  "$PYTHON" monitor.py >> "$LOG_FILE" 2>&1

EXIT_CODE=$?
echo "$(date '+%Y-%m-%d %H:%M:%S') Concluído (exit: $EXIT_CODE)" >> "$LOG_FILE"
exit $EXIT_CODE
