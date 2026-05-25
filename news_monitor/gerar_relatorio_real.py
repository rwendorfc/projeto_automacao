"""Gera relatório com notícias reais coletadas via WebSearch em 25/05/2026."""

import sys
from pathlib import Path
from datetime import datetime, timezone

sys.path.insert(0, str(Path(__file__).parent))

from news_fetcher import Noticia
from report_generator import gerar_html, gerar_json
from config import PESSOAS_MONITORADAS

_UTC = timezone.utc

NOTICIAS_REAIS = {
    "Ronaldo Caiado": [
        Noticia(
            titulo="Caiado volta a Minas para agenda com agro pela terceira vez em menos de um mês",
            url="https://www.otempo.com.br/eleicoes/2026/presidentes/2026/5/21/caiado-volta-a-minas-para-agenda-com-agro-pela-terceira-vez-em-menos-de-um-mes",
            fonte="O Tempo",
            publicado_em=datetime(2026, 5, 21, tzinfo=_UTC),
            resumo="Pré-candidato à presidência pelo PSD, Ronaldo Caiado realizou sua terceira agenda no agronegócio de Minas Gerais em menos de um mês. A estratégia faz parte de um plano para conquistar votos do centro e se distanciar da polarização bolsonarista.",
            pessoa="Ronaldo Caiado",
        ),
        Noticia(
            titulo="Quem é Ronaldo Caiado, aposta do PSD para o Planalto em 2026",
            url="https://www.congressoemfoco.com.br/noticia/117684/quem-e-ronaldo-caiado-aposta-do-psd-para-o-planalto-em-2026",
            fonte="Congresso em Foco",
            publicado_em=datetime(2026, 3, 30, tzinfo=_UTC),
            resumo="O PSD confirmou Ronaldo Caiado como candidato à presidência da República em 30 de março de 2026, após sua filiação ao partido em janeiro. Caiado é herdeiro de uma dinastia política goiana e liderança do setor rural, com avaliação positiva da gestão do estado.",
            pessoa="Ronaldo Caiado",
        ),
        Noticia(
            titulo="Eleições 2026: quem é Ronaldo Caiado, pré-candidato à presidência?",
            url="https://exame.com/brasil/eleicoes-2026-quem-e-ronaldo-caiado-pre-candidato-a-presidencia/",
            fonte="Exame",
            publicado_em=datetime(2026, 4, 10, tzinfo=_UTC),
            resumo="Perfil do governador licenciado de Goiás que disputará a presidência em 2026. O governo estadual aponta quedas superiores a 90% em alguns tipos de roubo e acima de 60% em homicídios entre 2018 e o primeiro semestre de 2025.",
            pessoa="Ronaldo Caiado",
        ),
    ],

    "Gracinha Caiado": [
        Noticia(
            titulo="Gracinha Caiado lidera intenções de voto para o Senado em Goiás",
            url="https://www.poder360.com.br/poder-eleicoes/gracinha-caiado-lidera-intencoes-de-voto-para-o-senado-em-goias/",
            fonte="Poder360",
            publicado_em=datetime(2026, 5, 7, tzinfo=_UTC),
            resumo="Gracinha Caiado, filiada ao União Brasil, lidera as intenções de voto para o Senado em Goiás com 39,1%, de acordo com pesquisa Paraná Pesquisas divulgada em abril de 2026. Ela é a principal nome da base governista para a disputa.",
            pessoa="Gracinha Caiado",
        ),
        Noticia(
            titulo="Paraná Pesquisas: Gracinha Caiado lidera corrida ao Senado com 36,9% em GO",
            url="https://exame.com/brasil/parana-pesquisas-gracinha-caiado-lidera-corrida-ao-senado-com-369-em-go/",
            fonte="Exame / Paraná Pesquisas",
            publicado_em=datetime(2026, 4, 7, tzinfo=_UTC),
            resumo="Levantamento do instituto Paraná Pesquisas aponta Gracinha Caiado com 36,9% das intenções de voto para o Senado Federal por Goiás, consolidando sua liderança na disputa para outubro de 2026.",
            pessoa="Gracinha Caiado",
        ),
        Noticia(
            titulo="Gracinha Caiado defende aliança com o PL e chapa única ao Senado em 2026",
            url="https://www.podergoias.com.br/materia/22391/gracinha-caiado-defende-alianca-com-o-pl-e-chapa-unica-ao-senado-em-2026",
            fonte="Poder Goiás",
            publicado_em=datetime(2026, 5, 10, tzinfo=_UTC),
            resumo="Em maio de 2026, Gracinha Caiado defendeu publicamente a aliança entre a base do governador Ronaldo Caiado e o Partido Liberal (PL) para as eleições. Ela defende a formação de uma chapa única com dois candidatos ao Senado.",
            pessoa="Gracinha Caiado",
        ),
        Noticia(
            titulo="Gracinha Caiado abre edição 2026 do Goiás Social Mulher em Goiânia",
            url="https://tv10.com.br/cidades/goias/gracinha-caiado-abre-edicao-2026-do-goias-social-mulher-em-goiania/",
            fonte="TV10",
            publicado_em=datetime(2026, 3, 5, tzinfo=_UTC),
            resumo="A ex-primeira-dama Gracinha Caiado abriu a edição 2026 do programa Goiás Social Mulher na Praça Cívica, centro de Goiânia, oferecendo serviços gratuitos de saúde, assistência social e emissão de documentos à população durante cinco dias.",
            pessoa="Gracinha Caiado",
        ),
        Noticia(
            titulo="Gracinha Caiado faz visita institucional ao TCMGO",
            url="https://www.tcmgo.tc.br/site/2026/03/gracinha-caiado-faz-visita-institucional-ao-tcmgo/",
            fonte="Tribunal de Contas dos Municípios de Goiás",
            publicado_em=datetime(2026, 3, 20, tzinfo=_UTC),
            resumo="Gracinha Caiado realizou visita institucional ao Tribunal de Contas dos Municípios do Estado de Goiás (TCMGO) em março de 2026, reforçando sua agenda política e institucional no estado.",
            pessoa="Gracinha Caiado",
        ),
    ],

    "Adryanna Caiado": [
        Noticia(
            titulo="OVG divulga resultado final do ProBem 2026/1 com cinco mil beneficiários",
            url="https://aredacao.com.br/ovg-divulga-resultado-final-do-probem-2026-1-com-cinco-mil-beneficiarios-selecionados/",
            fonte="A Redação / OVG",
            publicado_em=datetime(2026, 2, 10, tzinfo=_UTC),
            resumo="A Organização das Voluntárias de Goiás (OVG), sob direção-geral de Adryanna Caiado, divulgou o resultado final do ProBem 2026/1: 5 mil estudantes selecionados, sendo 1.250 bolsas integrais e 3.750 parciais. A diretora destacou que o índice IMCF-A garante justiça e transparência no processo.",
            pessoa="Adryanna Caiado",
        ),
        Noticia(
            titulo="ProBem 2026/1: 5 mil novos bolsistas universitários em Goiás",
            url="https://agenciacoradenoticias.go.gov.br/182715-governo-divulga-resultado-final-do-probem-2026-1-com-cinco-mil-beneficiarios-selecionados",
            fonte="Agência Cora de Notícias / Governo de Goiás",
            publicado_em=datetime(2026, 2, 10, tzinfo=_UTC),
            resumo="O Governo de Goiás, por meio do Goiás Social e OVG, liberou a lista final de bolsistas do ProBem 2026/1. As bolsas integrais cobrem até R$ 1.500 para cursos gerais e R$ 5.800 para Medicina. Adryanna Caiado, diretora-geral da OVG, ressaltou que jovens têm talento e o Estado deve garantir os meios de desenvolvê-lo.",
            pessoa="Adryanna Caiado",
        ),
        Noticia(
            titulo="Caiado deixa Governo de Goiás com ao menos 10 parentes em cargos",
            url="https://www.poder360.com.br/poder-eleicoes/caiado-deixa-governo-de-goias-com-ao-menos-10-parentes-em-cargos/",
            fonte="Poder360",
            publicado_em=datetime(2026, 3, 28, tzinfo=_UTC),
            resumo="Levantamento aponta que ao menos 10 parentes de Ronaldo Caiado ocupavam cargos no governo goiano quando o ex-governador deixou o estado para disputar a presidência. Adryanna Leonor Melo de Oliveira Caiado, casada com primo de Caiado, acumula cargos na OVG, Goiás Parcerias e Saneago.",
            pessoa="Adryanna Caiado",
        ),
    ],

    "Roberta Wendorf Carvalho": [],

    "Decio Wendorf": [],

    "Daniel Vilela": [
        Noticia(
            titulo="Daniel Vilela toma posse como governador de Goiás",
            url="https://goias.gov.br/abc/daniel-vilela-toma-posse-como-governador-de-goias/",
            fonte="Agência Brasil Central / Portal Goiás",
            publicado_em=datetime(2026, 3, 31, tzinfo=_UTC),
            resumo="Daniel Vilela foi empossado governador de Goiás em 31 de março de 2026 na Assembleia Legislativa em Goiânia, após a renúncia de Ronaldo Caiado para concorrer à presidência. Vilela ressaltou estabilidade institucional, foco em resultados e preservação do modelo de gestão que reposicionou Goiás no cenário nacional.",
            pessoa="Daniel Vilela",
        ),
        Noticia(
            titulo="Revista Veja aponta Daniel Vilela como 'exceção' entre aliados de governadores para 2026",
            url="https://www.jornalopcao.com.br/ultimas-noticias/revista-veja-aponta-daniel-vilela-como-excecao-entre-aliados-de-governadores-para-2026-829253/",
            fonte="Jornal Opção / Veja",
            publicado_em=datetime(2026, 4, 15, tzinfo=_UTC),
            resumo="A Revista Veja destacou Daniel Vilela como caso raro entre os aliados de governadores que disputarão eleições em 2026, indicando posicionamento político diferenciado do novo governador de Goiás no cenário nacional.",
            pessoa="Daniel Vilela",
        ),
        Noticia(
            titulo="Daniel Vilela reforça apoio ao agro em evento no Vale do Araguaia",
            url="https://transmissaopolitica.com.br/politica-goiana/2026/05/06/daniel-vilela-apoio-agro-vale-do-araguaia/",
            fonte="Transmissão Política",
            publicado_em=datetime(2026, 5, 6, tzinfo=_UTC),
            resumo="O governador Daniel Vilela participou em 6 de maio da 2ª edição da Conforto Experience, em Nova Crixás, no Vale do Araguaia. Ele defendeu o diálogo direto com o setor produtivo e afirmou que o Governo de Goiás tem ouvido as demandas dos produtores para orientar novas políticas públicas.",
            pessoa="Daniel Vilela",
        ),
    ],

    "Iara Netto Vilela": [
        Noticia(
            titulo="Iara Netto Vilela assume o Gabinete de Políticas Sociais em Goiás",
            url="https://www.revistastile.com.br/iara-netto-vilela-assume-o-gabinete-de-politicas-sociais-em-goias/",
            fonte="Revista Stile",
            publicado_em=datetime(2026, 4, 2, tzinfo=_UTC),
            resumo="Iara Netto Vilela, primeira-dama de Goiás, assumiu o comando do Gabinete de Políticas Sociais (GPS) do estado. Formada em Administração pela PUC-GO e ex-empresária do setor calçadista, ela também preside honorariamente a OVG.",
            pessoa="Iara Netto Vilela",
        ),
        Noticia(
            titulo="Daniel e Iara Vilela lançam Goiás Social em Formosa com 1,5 mil cartões e serviços",
            url="https://www.diariogoianiense.com.br/noticia/daniel-e-iara-vilela-lancam-goias-social-em-formosa-com-1-5-mil-cartoes-e-servicos",
            fonte="Diário Goianiense",
            publicado_em=datetime(2026, 5, 19, tzinfo=_UTC),
            resumo="O governador Daniel Vilela e a primeira-dama Iara Netto Vilela inauguraram etapa do Goiás Social em Formosa em 19 de maio de 2026, distribuindo serviços gratuitos de saúde, assistência social e documentação, com previsão de mais de 1.500 cartões para famílias em vulnerabilidade.",
            pessoa="Iara Netto Vilela",
        ),
        Noticia(
            titulo="PF prende sogra do governador de Goiás em operação contra migração ilegal",
            url="https://www.cartacapital.com.br/politica/pf-prende-a-sogra-do-governador-de-goias-em-operacao-contra-migracao-ilegal/",
            fonte="CartaCapital",
            publicado_em=datetime(2026, 5, 7, tzinfo=_UTC),
            resumo="A Polícia Federal prendeu Maria Helena de Souza Costa, mãe de Iara Netto Vilela e sogra do governador Daniel Vilela, na Operação Travessia em 7 de maio de 2026. Ela é suspeita de chefiar um dos grupos investigados pelo tráfico ilegal de pessoas, que movimentou R$ 240 milhões entre 2018 e 2023. A PF informou que Daniel Vilela e Iara Netto Vilela não são alvos da investigação.",
            pessoa="Iara Netto Vilela",
        ),
        Noticia(
            titulo="Goiás Social abre mais de mil vagas para cursos gratuitos de robótica em 21 cidades",
            url="https://www.jornalestadodegoias.com.br/2026/05/24/robotica-e-tecnologia-goias-social-abre-mais-de-mil-vagas-para-cursos-gratuitos-em-21-cidades/",
            fonte="Jornal Estado de Goiás",
            publicado_em=datetime(2026, 5, 24, tzinfo=_UTC),
            resumo="O programa Goiás Social, coordenado por Iara Netto Vilela, abriu mais de mil vagas para cursos gratuitos de robótica e tecnologia em 21 cidades do estado, ampliando o acesso de jovens vulneráveis a áreas estratégicas para o futuro profissional.",
            pessoa="Iara Netto Vilela",
        ),
        Noticia(
            titulo="'Seguiremos ampliando o cuidado social em Goiás', destaca Iara Netto Vilela",
            url="https://sdnews.com.br/noticia/15476/seguiremos-ampliando-o-cuidado-social-e-fortalecendo-oportunidades-em-goias-destaca-iara-netto-vile.html",
            fonte="Serra Dourada News",
            publicado_em=datetime(2026, 4, 20, tzinfo=_UTC),
            resumo="Iara Netto Vilela destacou o compromisso do Governo de Goiás em ampliar o cuidado social e fortalecer oportunidades para a população em situação de vulnerabilidade, com foco em programas de inclusão e geração de renda.",
            pessoa="Iara Netto Vilela",
        ),
    ],
}


def main():
    resultados = []
    for pessoa in PESSOAS_MONITORADAS:
        noticias = NOTICIAS_REAIS.get(pessoa["nome"], [])
        resultados.append({"pessoa": pessoa, "noticias": noticias})

    caminho_html = gerar_html(resultados, "resultados")
    caminho_json = gerar_json(resultados, "resultados")

    print("\n" + "=" * 60)
    print(" MONITORAMENTO DE NOTÍCIAS REAIS — 25/05/2026")
    print("=" * 60)
    for item in resultados:
        n = len(item["noticias"])
        marcador = "●" if n else "○"
        print(f"\n{marcador} {item['pessoa']['nome']}  ({n} notícia(s))")
        for noticia in item["noticias"]:
            print(f"   · {noticia.titulo[:65]}")
    print("\n" + "=" * 60)
    print(f"\nRelatório HTML → {caminho_html}")
    print(f"Dados JSON     → {caminho_json}")


if __name__ == "__main__":
    main()
