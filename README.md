# Monitoramento de Notícias com Análise de Sentimento

Sistema automatizado de monitoramento de notícias para personalidades públicas goianas, com análise de sentimento via Claude AI.

## Pessoas monitoradas

| Nome | Cargo |
|------|-------|
| Gracinha Caiado | Primeira-dama de Goiás |
| Ronaldo Caiado | Governador de Goiás |
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

## Estrutura dos arquivos gerados

```
resultados/
├── relatorio.html    ← relatório visual (abra no navegador)
└── resultados.json   ← dados estruturados em JSON
```

## Estrutura do projeto

```
news_monitor/
├── config.py             # configurações e lista de pessoas
├── news_fetcher.py       # coleta de notícias (Google News RSS + NewsAPI)
├── sentiment_analyzer.py # análise de sentimento via Claude API
├── report_generator.py   # geração de relatórios HTML e JSON
├── demo_data.py          # dados mockados para demonstração
├── monitor.py            # ponto de entrada principal
└── setup.py              # instalação e verificação do ambiente
```

## Automatização (cron)

Para executar diariamente às 7h:

```cron
0 7 * * * cd /caminho/projeto/news_monitor && ANTHROPIC_API_KEY=sk-ant-... python monitor.py >> /var/log/news_monitor.log 2>&1
```
