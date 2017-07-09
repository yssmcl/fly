# TODO: checar se os objetos não são nulos antes de colocar no PDF
# TODO: limpar os imports (ou baixar plugin que limpa e adiciona sozinho)
from pylatex import Document, Enumerate, NoEscape, Package, Tabularx, FlushRight, \
     LineBreak, NewLine, MultiColumn, MultiRow, HFill, Table, PageStyle, Head, \
     simple_page_number, Foot, Figure, StandAloneGraphic
from pylatex.base_classes import Environment
from pylatex.frames import MdFramed
from pylatex.utils import escape_latex, bold

from base.models import *
from curso_extensao.models import *
from base import pdfutils

def gerar_pdf(curso):
    # Pacotes e configurações
    doc = pdfutils.init_document()

    doc.packages.add(Package('microtype'))
    doc.packages.add(Package('indentfirst'))
    doc.packages.add(Package('graphicx'))
    doc.packages.add(Package('float'))
    doc.packages.add(Package('titlesec'))
    doc.packages.add(Package('parskip'))
    doc.packages.add(Package('enumitem'))
    doc.packages.add(Package('helvet'))
    doc.packages.add(Package('tabularx'))
    doc.packages.add(Package('mdframed'))
    doc.packages.add(Package('eqparbox'))
    doc.packages.add(Package('fancyhdr'))
    # TODO:
    #  doc.packages.add(Package('hyphenat', options='none')) # impede hifenização

    # TODO:
    #  doc.append(NoEscape(r'\fontfamily{\sfdefault}\selectfont'))
    doc.preamble.append(NoEscape(r'\renewcommand{\familydefault}{\sfdefault}'))

    # Configuração das listas
    doc.preamble.append(NoEscape(r'''
\setlist[enumerate, 1]{label*=\textbf{\arabic*}, leftmargin=*}
\setlist[enumerate, 2]{label*=\textbf{.\arabic*}, leftmargin=*}
    '''))

    doc.preamble.append(NoEscape('\pagestyle{fancy}'))

    # Início do documento
    doc.append(NoEscape(r'\footnotesize'))

    pdfutils.cabecalho(doc)

    pdfutils.rodape(doc, 'ANEXO V DA RESOLUÇÃO Nº 236/2014-CEPE, DE 13 DE NOVEMBRO DE 2014')

    doc.append(NoEscape(r'\texttt{ANEXO V DA RESOLUÇÃO Nº 236/2014-CEPE, DE 13 DE NOVEMBRO DE 2014}'))

    pdfutils.titulo(doc, 'FORMULÁRIO ESPECÍFICO PARA ATIVIDADES DE EXTENSÃO', 'MODALIDADE CURSO DE EXTENSÃO')

    doc.append(NoEscape('\hrulefill'))

    # Início do formulário
    with doc.create(Enumerate()) as enum:
        pdfutils.item(doc, enum, 'TÍTULO: ', curso.titulo)

        pdfutils.item(doc, enum, 'COORDENADOR(a): ', curso.coordenador.nome_completo)

        periodo_inicio = curso.periodo_realizacao_inicio.strftime('%d/%m/%Y')
        periodo_fim = curso.periodo_realizacao_fim.strftime('%d/%m/%Y')
        periodo_realizacao = 'de {} a {}'.format(periodo_inicio, periodo_fim)
        pdfutils.item(doc, enum, 'PERÍODO DE REALIZAÇÃO: ', periodo_realizacao)

        pdfutils.mdframed_informar(doc, enum, curso)

        pdfutils.tabela_unidade_administrativa(doc, enum, curso)

        pdfutils.tabela_centro(doc, enum, curso)

        pdfutils.tabela_grande_area(doc, enum, id=curso.grande_area.id)

        pdfutils.tabela_palavras_chave(doc, enum)

        pdfutils.tabela_area_tematica_principal(doc, enum, curso, id=curso.area_tematica_principal.id)

        pdfutils.tabela_area_tematica_secundaria(doc, enum, curso, id=curso.area_tematica_secundaria.id)

        pdfutils.tabela_linha_extensao(doc, enum, curso, id=curso.linha_extensao.id)

        pdfutils.item(doc, enum, 'PÚBLICO ALVO: ', curso.publico_alvo)

        pdfutils.item(doc, enum, 'NÚMERO DE PESSOAS A SEREM BENEFICIADAS: ', curso.numero_pessoas_beneficiadas)

        pdfutils.item(doc, enum, 'CARGA HORÁRIA TOTAL: ', curso.carga_horaria_total)

        pdfutils.item(doc, enum, 'Nº DE VAGAS: ', curso.numero_vagas)

        pdfutils.item(doc, enum, 'LOCAL DA INSCRIÇÃO: ', curso.local_inscricao)

        pdfutils.item(doc, enum, 'RESUMO: ')
        doc.append(NewLine())
        doc.append(escape_latex(curso.resumo))

        pdfutils.item(doc, enum, 'PROGRAMAÇÃO: ', curso.programacao)

        pdfutils.item(doc, enum, 'EQUIPE DE TRABALHO: ')
        doc.append(NewLine())
        pdfutils.mdframed_equipe_trabalho(doc, enum, curso)

        pdfutils.item(doc, enum, 'DISCENTES UNIOESTE: ')
        doc.append(NewLine())
        pdfutils.tabela_discentes(doc, enum, curso)

        pdfutils.item(doc, enum, 'MEMBROS DA COMUNIDADE / PARTICIPANTES EXTERNOS: ')
        doc.append(NewLine())
        pdfutils.tabela_membros(doc, enum, curso)

        # Checa antes pois a previsão orçamentária não é obrigatório
        # TODO: previsão orçamentária é obrigatório?
        if PrevisaoOrcamentaria_CursoExtensao.objects.filter(curso_extensao=curso.id):
            previsao_orcamentaria = PrevisaoOrcamentaria_CursoExtensao.objects.get(curso_extensao=curso.id)

            pdfutils.tabela_previsao_orcamentaria(doc, enum, previsao_orcamentaria)

            pdfutils.tabela_gestao_recursos_financeiros(doc, enum, previsao_orcamentaria)

    doc.generate_pdf('curso_extensao/pdf/curso_extensao_' + str(curso.id))
