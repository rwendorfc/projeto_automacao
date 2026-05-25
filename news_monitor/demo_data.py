"""Dados mockados para demonstração e testes sem acesso à rede."""

from datetime import datetime, timezone, timedelta
from news_fetcher import Noticia

_AGORA = datetime.now(tz=timezone.utc)
_D = lambda days: _AGORA - timedelta(days=days)


NOTICIAS_DEMO = {
    "Ronaldo Caiado": [
        Noticia(
            titulo="Caiado anuncia R$ 500 milhões em investimentos para infraestrutura de Goiás",
            url="https://exemplo.com/caiado-investimentos",
            fonte="Jornal O Popular",
            publicado_em=_D(0),
            resumo="O governador Ronaldo Caiado assinou pacote de investimentos em rodovias e saneamento para 50 municípios goianos.",
            pessoa="Ronaldo Caiado",
        ),
        Noticia(
            titulo="Caiado defende reforma tributária e critica impacto nos estados",
            url="https://exemplo.com/caiado-reforma",
            fonte="Folha de Goiás",
            publicado_em=_D(1),
            resumo="Em encontro com governadores, Caiado afirmou que a reforma tributária prejudica os estados produtores do agronegócio.",
            pessoa="Ronaldo Caiado",
        ),
        Noticia(
            titulo="Índice de aprovação do governo Caiado chega a 68%, aponta pesquisa",
            url="https://exemplo.com/aprovacao-caiado",
            fonte="Datafolha Regional",
            publicado_em=_D(2),
            resumo="Pesquisa de opinião aponta que 68% dos goianos aprovam a gestão do governador Ronaldo Caiado.",
            pessoa="Ronaldo Caiado",
        ),
        Noticia(
            titulo="TCE aponta irregularidades em contratos da Secretaria de Saúde de Goiás",
            url="https://exemplo.com/tce-saude",
            fonte="Metrópoles Goiás",
            publicado_em=_D(3),
            resumo="Tribunal de Contas do Estado identificou sobrepreço em licitações de medicamentos na gestão estadual.",
            pessoa="Ronaldo Caiado",
        ),
        Noticia(
            titulo="Governador inaugura hospital regional em Anápolis",
            url="https://exemplo.com/hospital-anapolis",
            fonte="Agência Goiás",
            publicado_em=_D(4),
            resumo="Caiado participou da inauguração do Hospital Regional de Anápolis, unidade com 200 leitos.",
            pessoa="Ronaldo Caiado",
        ),
    ],
    "Gracinha Caiado": [
        Noticia(
            titulo="Gracinha Caiado lança programa de capacitação profissional para mulheres em Goiás",
            url="https://exemplo.com/gracinha-mulheres",
            fonte="Globo Goiás",
            publicado_em=_D(0),
            resumo="A primeira-dama Gracinha Caiado lançou o programa 'Goiás Mulher' voltado à qualificação profissional de 10 mil mulheres vulneráveis.",
            pessoa="Gracinha Caiado",
        ),
        Noticia(
            titulo="Primeira-dama visita entidades sociais no interior goiano",
            url="https://exemplo.com/gracinha-visita",
            fonte="O Popular",
            publicado_em=_D(2),
            resumo="Gracinha Caiado percorreu municípios do interior em ação de doação de cestas básicas e acompanhamento de projetos sociais.",
            pessoa="Gracinha Caiado",
        ),
        Noticia(
            titulo="Gracinha Caiado representa Goiás em evento sobre saúde da mulher em Brasília",
            url="https://exemplo.com/gracinha-brasilia",
            fonte="Correio Braziliense",
            publicado_em=_D(4),
            resumo="A primeira-dama participou do Fórum Nacional de Saúde da Mulher e apresentou iniciativas goianas.",
            pessoa="Gracinha Caiado",
        ),
    ],
    "Adryanna Caiado": [
        Noticia(
            titulo="Adryanna Caiado participa de ação de preservação ambiental no Cerrado",
            url="https://exemplo.com/adryanna-cerrado",
            fonte="Greenpeace Brasil / Agência Goiás",
            publicado_em=_D(1),
            resumo="Filha do governador participou de mutirão de reflorestamento no Parque Estadual da Serra de Jaraguá.",
            pessoa="Adryanna Caiado",
        ),
        Noticia(
            titulo="Adryanna Caiado defende ampliação de políticas de saúde mental em evento nacional",
            url="https://exemplo.com/adryanna-saude-mental",
            fonte="Veja Saúde",
            publicado_em=_D(3),
            resumo="Em palestra em São Paulo, Adryanna Caiado falou sobre a importância de políticas públicas de saúde mental para jovens.",
            pessoa="Adryanna Caiado",
        ),
    ],
    "Roberta Wendorf Carvalho": [
        Noticia(
            titulo="Roberta Wendorf Carvalho é empossada no Conselho Estadual de Cultura de Goiás",
            url="https://exemplo.com/roberta-conselho-cultura",
            fonte="Agência Goiás",
            publicado_em=_D(1),
            resumo="Cerimônia de posse marcou a entrada de Roberta Wendorf Carvalho como conselheira do colegiado cultural goiano.",
            pessoa="Roberta Wendorf Carvalho",
        ),
        Noticia(
            titulo="Investimento em cultura: Goiás destina R$ 8 milhões para festivais regionais",
            url="https://exemplo.com/cultura-festivais",
            fonte="Folha de Goiás",
            publicado_em=_D(3),
            resumo="Com participação ativa do conselho estadual, Goiás anuncia edital para apoio a festivais de cultura popular.",
            pessoa="Roberta Wendorf Carvalho",
        ),
    ],
    "Decio Wendorf": [
        Noticia(
            titulo="Décio Wendorf participa de reunião do setor empresarial em Goiânia",
            url="https://exemplo.com/decio-empresarial",
            fonte="Diário do Comércio Goiás",
            publicado_em=_D(2),
            resumo="Encontro reuniu líderes do setor produtivo para discutir o cenário econômico de Goiás no segundo semestre.",
            pessoa="Decio Wendorf",
        ),
    ],
    "Daniel Vilela": [
        Noticia(
            titulo="Daniel Vilela fortalece candidatura ao governo de Goiás com apoios regionais",
            url="https://exemplo.com/daniel-vilela-candidatura",
            fonte="O Popular",
            publicado_em=_D(0),
            resumo="O presidente do MDB goiano articula apoios de prefeitos e lideranças do interior para a disputa eleitoral de 2026.",
            pessoa="Daniel Vilela",
        ),
        Noticia(
            titulo="Vilela critica política de segurança pública do estado e propõe alternativas",
            url="https://exemplo.com/vilela-seguranca",
            fonte="Metrópoles Goiás",
            publicado_em=_D(1),
            resumo="Daniel Vilela apresentou proposta de reestruturação da segurança pública para Goiás em evento do MDB.",
            pessoa="Daniel Vilela",
        ),
        Noticia(
            titulo="MDB goiano realiza convenção e confirma Daniel Vilela como pré-candidato",
            url="https://exemplo.com/mdb-convencao",
            fonte="Globo Goiás",
            publicado_em=_D(2),
            resumo="Convenção regional do MDB formalizou a pré-candidatura de Daniel Vilela ao governo do estado.",
            pessoa="Daniel Vilela",
        ),
        Noticia(
            titulo="Ficha limpa: Daniel Vilela enfrenta questionamentos sobre financiamento de campanha anterior",
            url="https://exemplo.com/vilela-campanha-anterior",
            fonte="Poder360",
            publicado_em=_D(4),
            resumo="Documentos revelam questionamentos do TSE sobre prestação de contas de campanha passada.",
            pessoa="Daniel Vilela",
        ),
    ],
    "Iara Netto Vilela": [
        Noticia(
            titulo="Iara Netto Vilela lidera projeto de alfabetização em comunidades rurais de Goiás",
            url="https://exemplo.com/iara-alfabetizacao",
            fonte="Agência Goiás",
            publicado_em=_D(1),
            resumo="O projeto coordenado por Iara Netto Vilela já beneficiou mais de 2 mil adultos em zonas rurais do estado.",
            pessoa="Iara Netto Vilela",
        ),
        Noticia(
            titulo="Iara Vilela é homenageada pela OAB-GO por atuação em direitos humanos",
            url="https://exemplo.com/iara-oab-homenagem",
            fonte="OAB Goiás / Jornal Jurídico",
            publicado_em=_D(3),
            resumo="A OAB seccional Goiás entregou medalha de mérito a Iara Netto Vilela por sua contribuição aos direitos humanos.",
            pessoa="Iara Netto Vilela",
        ),
    ],
}


def gerar_noticias_demo(pessoa: dict) -> list[Noticia]:
    """Retorna notícias de demonstração para uma pessoa."""
    nome = pessoa["nome"]
    noticias = NOTICIAS_DEMO.get(nome, [])
    for n in noticias:
        n.pessoa = nome
    return noticias
