#!/bin/bash
# Instala o cron job para executar o monitoramento a cada 4 horas.
# Execute uma única vez: bash install_cron.sh

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WRAPPER="$SCRIPT_DIR/run_monitor.sh"

chmod +x "$WRAPPER"

# Linha cron: a cada 4 horas (0h, 4h, 8h, 12h, 16h, 20h)
CRON_LINE="0 */4 * * * $WRAPPER"

# Verifica se já existe para não duplicar
if crontab -l 2>/dev/null | grep -qF "$WRAPPER"; then
    echo "Cron job já instalado:"
    crontab -l | grep "$WRAPPER"
    exit 0
fi

# Adiciona ao crontab atual
(crontab -l 2>/dev/null; echo "$CRON_LINE") | crontab -

echo "Cron job instalado com sucesso!"
echo ""
echo "Agendamento: a cada 4 horas (0h, 4h, 8h, 12h, 16h, 20h)"
echo "Comando    : $CRON_LINE"
echo "Log        : $SCRIPT_DIR/logs/cron.log"
echo ""
echo "Para verificar: crontab -l"
echo "Para remover  : crontab -e  (e apague a linha)"
