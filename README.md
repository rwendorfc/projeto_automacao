# Monitoramento de Notícias com Análise de Sentimento

Sistema automatizado de monitoramento de notícias para personalidades públicas goianas, com análise de sentimento via Claude AI.

## Pessoas monitoradas

| Nome | Cargo |
|------|-------|
| Gracinha Caiado | Ex-Primeira-dama de Goiás |
| Ronaldo Caiado | Ex-Governador de Goiás |
| Adryanna Caiado | Família Caiado |
| Roberta Wendorf Carvalho | Personalidade pública |
| Decio Wendorf | Personalidade pública |
| Daniel Vilela | Político de Goiás |
| Iara Netto Vilela | Personalidade pública |

## Funcionalidades

- **Coleta automática** de notícias via Google News RSS (últimos 7 dias)
- **Análise de sentimento** via Claude AI (Positivo / Negativo / Neutro / Misto)
- **Score numérico** de -1.0 (muito negativo) a +1.0 (muito positivo)
- **Extração de temas** relevantes por notícia
- **Relatório HTML** interativo e visualmente organizado
- **Export JSON** com todos os dados estruturados
- **Modo demo** para testes sem acesso à rede
- **Agendamento automático** a cada 4 horas com histórico de execuções

## Instalação

```bash
git clone https://github.com/rwendorfc/projeto_automacao
cd projeto_automacao

pip install -r requirements.txt
```

## Configuração

```bash
# Obrigatório para análise de sentimento
export ANTHROPIC_API_KEY="sk-ant-..."

# Opcional — aumenta cobertura de notícias (https://newsapi.org)
export NEWSAPI_KEY="sua-chave-newsapi"
```

## Uso

```bash
cd news_monitor

# Monitoramento completo (requer ANTHROPIC_API_KEY + acesso à internet)
python monitor.py

# Modo demonstração com dados mockados (não requer rede nem API key)
python monitor.py --demo

# Monitorar apenas uma pessoa
python monitor.py --pessoa "Ronaldo Caiado"

# Sem análise de sentimento (apenas coleta notícias)
python monitor.py --sem-sentimento

# Definir diretório de saída
python monitor.py --saida /caminho/para/saida
```

## Agendamento (a cada 4 horas)

### Opção 1 — Daemon Python (recomendado)

```bash
cd news_monitor

# Inicia o daemon (roda indefinidamente, Ctrl+C para parar)
python scheduler.py

# Verificar próxima execução
python scheduler.py --status

# Executar uma vez imediatamente
python scheduler.py --uma-vez
```

### Opção 2 — Cron

```bash
# Instala automaticamente o cron job (a cada 4h: 0h, 4h, 8h, 12h, 16h, 20h)
bash news_monitor/install_cron.sh

# Verificar: crontab -l
# Remover:   crontab -e
```

### Opção 3 — systemd (servidores Linux)

```bash
# Copie os arquivos de unidade
sudo cp news_monitor/systemd/news-monitor.service /etc/systemd/system/
sudo cp news_monitor/systemd/news-monitor.timer   /etc/systemd/system/

# Edite o .service com seu usuário e caminho real
sudo nano /etc/systemd/system/news-monitor.service

# Ative e inicie
sudo systemctl daemon-reload
sudo systemctl enable --now news-monitor.timer

# Verificar status
sudo systemctl status news-monitor.timer
sudo journalctl -u news-monitor.service -f
```

## Estrutura dos arquivos gerados

Cada execução cria um subdiretório com timestamp; `latest/` aponta para a mais recente.

```
resultados/
├── latest/               ← symlink para a execução mais recente
├── 2026-05-25_06-00/
│   ├── relatorio.html
│   └── resultados.json
├── 2026-05-25_10-00/
│   ├── relatorio.html
│   └── resultados.json
└── ...                   ← mantém as últimas 24 execuções (6 dias)
```

## Estrutura do projeto

```
news_monitor/
├── config.py              # configurações, pessoas e intervalo (INTERVALO_HORAS = 4)
├── news_fetcher.py        # coleta via Google News RSS + NewsAPI
├── sentiment_analyzer.py  # análise de sentimento via Claude API
├── report_generator.py    # relatórios HTML e JSON
├── demo_data.py           # dados mockados para demonstração
├── monitor.py             # execução manual (CLI)
├── scheduler.py           # daemon de agendamento (a cada 4h)
├── run_monitor.sh         # wrapper para cron
├── install_cron.sh        # instalador do cron job
├── setup.py               # verificação do ambiente
└── systemd/               # unidades systemd (serviços de servidor)
    ├── news-monitor.service
    └── news-monitor.timer
```
