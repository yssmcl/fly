from pylatex import NoEscape, FlushRight, NewLine, MdFramed, Enumerate, Document, \
     NewPage, HFill, Tabularx, LineBreak, MultiColumn, MultiRow, Package, Center, \
     MiniPage
from pylatex.utils import escape_latex, bold

from base.models import *
from curso_extensao.models import *
from relatorio.models import *


mdframed_options = ['innertopmargin=5pt, innerleftmargin=3pt, innerrightmargin=3pt']
width_argument = NoEscape(r'\linewidth')


def init_document():
    geometry_options = {'left': '3cm',
                        'right': '2cm',
                        'bottom': '2cm',
                        'top': '6.5cm',
                        'headheight': '5cm'}
    document = Document(geometry_options=geometry_options, lmodern=False, document_options=['12pt', 'a4paper', 'oneside'])

    return document


def pacotes(doc):
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
    # Impede hifenização das palavras
    # doc.packages.add(Package('hyphenat', options='none'))

def configuracoes_preambulo(doc):
    doc.preamble.append(NoEscape(r'\renewcommand{\familydefault}{\sfdefault}'))
    # doc.append(NoEscape(r'\fontfamily{\sfdefault}\selectfont'))

    # Configuração das listas
    doc.preamble.append(NoEscape(r'''
\setlist[enumerate, 1]{label*=\textbf{\arabic*}, leftmargin=*}
\setlist[enumerate, 2]{label*=\textbf{.\arabic*}, leftmargin=*}
    '''))

    # Configuração dos cabeçalhos
    doc.preamble.append(NoEscape('\pagestyle{fancy}'))

    # Diretório das imagens (relativo a relatorio/pdf/)
    doc.preamble.append(NoEscape(r'\graphicspath{{../../base/img/}}'))

    # Tamanho da fonte
    doc.append(NoEscape(r'\footnotesize'))

def cabecalho(doc):
    cabecalho = r'''
\renewcommand{\headrulewidth}{0pt}%
\renewcommand{\footrulewidth}{0pt}%
\fancyhead[L]{%
    \includegraphics[width=200px]{logo_unioeste.png}
    \newline
    \newline
    {\scriptsize
        Reitoria - CNPJ 78680337/0001-84 \\
        Rua Universitária, 1619 - Fone: (45) 3220-3000 - Fax: (45) 3324-4590 \\
        Jardim Universitário - Cx. P. 000701 - CEP 85819-110 - Cascavel - Paraná \\
        www.unioeste.br
    }
}
\fancyhead[R]{
    \includegraphics[width=80px]{logo_governo.jpg}
}
    '''

    doc.append(NoEscape(cabecalho))


def rodape(doc, texto):
    rodape = r'''
\fancyfoot[R]{
    {\footnotesize %(texto)s}
}
\fancyfoot[L]{
    \thepage
}
\fancyfoot[C]{}
    '''

    rodape = rodape % {'texto': texto}
    doc.append(NoEscape(rodape))


def titulo(doc, titulo, subtitulo):
    eqparbox = r'''
\eqparbox{a}{\relax\ifvmode\raggedleft\fi
    \underline{%(titulo)s} \\
    \bigskip
    %(subtitulo)s
}
\eqparbox{b}{
    \includegraphics[width=100px]{logo_extensao.jpg}
}
    '''

    eqparbox = eqparbox % {'titulo': titulo, 'subtitulo': subtitulo}
    flush_right = FlushRight()
    flush_right.append(NoEscape(eqparbox))
    doc.append(flush_right)


def item(doc, enum, texto, dado=None):
    enum.add_item(bold(texto))
    if dado:
        doc.append(escape_latex(dado))


def mdframed_informar(doc, enum, programa_extensao):
    with doc.create(MdFramed(options=mdframed_options)):
        item(doc, enum, 'INFORMAR: ')
        with doc.create(Enumerate()) as subenum:
            doc.append(NoEscape('\scriptsize'))

            subenum.add_item(NoEscape('Esta atividade faz parte de algum Programa de Extensão? '))
            if programa_extensao:
                doc.append(NoEscape(r'Não () Sim ({$\times$}): Qual? '))
                doc.append(programa_extensao.nome)
            else:
                doc.append(NoEscape(r'Não ($\times$) Sim (): Qual? '))

            doc.append(NoEscape(r'''
            Coordenador(a) do Programa: \\ \\ \\
            Assinatura: \hrulefill \\
            '''))

            # TODO: ???
            subenum.add_item('Esta Atividade de Extensão está articulada (quando for o caso): ao Ensino () à Pesquisa ()')


def tabela_unidade_administrativa(doc, enum, unidade_administrativa, campus):
        item(doc, enum, 'UNIDADE ADMINISTRATIVA: ')
        for ua in UnidadeAdministrativa.objects.all():
            if unidade_administrativa and unidade_administrativa.id == ua.id:
                doc.append(NoEscape(ua.nome + r' ($\times$) '))
            else:
                doc.append(ua.nome + ' () ')
        doc.append(NewLine())

        doc.append(bold('CAMPUS DE: '))
        for c in Campus.objects.all():
            if campus and campus.id == c.id:
                doc.append(NoEscape(campus.nome + r' ($\times$) '))
            else:
                doc.append(campus.nome + ' () ')


def tabela_centro(doc, enum, centro):
    item(doc, enum, 'CENTRO: ')
    doc.append(NewLine())
    for c in Centro.objects.all():
        if centro and centro.id == c.id:
            doc.append(NoEscape(centro.nome + r' ($\times$) '))
        else:
            doc.append(centro.nome + ' () ')


# id é opcional, só se quiser preencher a tabela
def tabela_alternativas(doc, model, table_spec, id=None, hline=True):
    from pylatex import Tabularx, NoEscape

    # Conta a quantidade de 'X', 'l', 'c', 'r' etc.
    nro_colunas = sum(char.isalpha() for char in table_spec)

    with doc.create(Tabularx(table_spec, width_argument=NoEscape('\linewidth'))) as tab:
        if hline:
            tab.add_hline()

        row = []
        for i, model in enumerate(model.objects.all(), 1):
            if id and model.id == id:
                row.append(NoEscape(r'($\times$) ' + model.nome))
            else:
                row.append('() ' + model.nome)

            if i%nro_colunas == 0:
                tab.add_row(row)
                del row[:]

        # Adiciona o resto dos itens à tabela
        for i in range(nro_colunas-len(row)):
            row.append('')
        tab.add_row(row)
        if hline: tab.add_hline()


def tabela_grande_area(doc, enum, id=None):
    item(doc, enum, 'GRANDE ÁREA: ')
    doc.append(NewLine())
    tabela_alternativas(doc, GrandeArea, '|X|X|X|', id=id)


def tabela_palavras_chave(doc, enum, model):
    item(doc, enum, 'PALAVRAS-CHAVE: ')
    doc.append(NewLine())

    nro_colunas = 3
    with doc.create(Tabularx('|X|X|X|', width_argument=NoEscape('\linewidth'))) as tab:
        tab.add_hline()

        row = []
        for i, model in enumerate(model.objects.all(), 1):
            row.append('{} ‒ {}'.format(str(i), model.nome))

            if i%nro_colunas == 0:
                tab.add_row(row)
                del row[:]

        # Adiciona o resto dos itens à tabela
        for i in range(nro_colunas-len(row)):
            row.append('')
        tab.add_row(row)

        tab.add_hline()


def tabela_area_tematica_principal(doc, enum, id):
    item(doc, enum, 'ÁREA TEMÁTICA PRINCIPAL: ')
    doc.append(NewLine())
    tabela_alternativas(doc, AreaTematica, '|X|X|X|', id=id)


def tabela_area_tematica_secundaria(doc, enum, area_tematica_secundaria, id):
    item(doc, enum, 'ÁREA TEMÁTICA SECUNDÁRIA: ')
    doc.append(NewLine())
    if area_tematica_secundaria:
        tabela_alternativas(doc, AreaTematica, '|X|X|X|', id=id)
    else:
        tabela_alternativas(doc, AreaTematica, '|X|X|X|')


def tabela_linha_extensao(doc, enum, linha_extensao, id):
    doc.append(NewPage())
    item(doc, enum, 'LINHA DE EXTENSÃO: ')
    doc.append(NewLine())
    doc.append(NewLine())
    doc.append(NoEscape(r'{\tiny'))
    if linha_extensao:
        tabela_alternativas(doc, LinhaExtensao, 'X|X|X', id=id, hline=False)
    doc.append(NoEscape('}'))


def mdframed_equipe_trabalho(doc, enum, projeto_extensao):
    # TODO: se projeto_extensao.servidores.all() for vazio, esse item não aparece?
    for servidor in projeto_extensao.servidores.all():
        servidor_cursoextensao = Servidor_CursoExtensao.objects.get(servidor_id=servidor.id)

        with doc.create(MdFramed(options=mdframed_options)):
            doc.append(bold('SERVIDORES UNIOESTE '))
            doc.append(NewLine())

            doc.append(NoEscape('Nome completo: '))
            doc.append(servidor.nome_completo)
            doc.append(NewLine())

            for tipo_servidor in TipoServidor.objects.all():
                if servidor.tipo.id == tipo_servidor.id:
                    doc.append(NoEscape(r' ($\times$) ' + tipo_servidor.nome + ' '))
                else:
                    doc.append(' () ' + tipo_servidor.nome + ' ')
            doc.append(NewLine())

            doc.append('Regime de trabalho: ')
            doc.append(escape_latex(servidor.regime_trabalho))
            doc.append(NoEscape('\ hora(s) \hfill'))
            doc.append('Carga horária semanal dedicada à atividade: ')
            doc.append(servidor_cursoextensao.carga_horaria_dedicada)
            doc.append(NoEscape('\ hora(s) \hfill'))
            doc.append(NewLine())

            doc.append('Colegiado: ')
            doc.append(escape_latex(servidor.colegiado))
            doc.append(HFill())
            doc.append('Centro: ')
            doc.append(escape_latex(servidor.centro.nome))
            doc.append(NewLine())

            doc.append('Unidade Administrativa: ')
            for ua in UnidadeAdministrativa.objects.all():
                if servidor.unidade_administrativa and servidor.unidade_administrativa.id == ua.id:
                    doc.append(NoEscape(r'($\times$) ' + ua.nome + ' '))
                else:
                    doc.append('() ' + ua.nome + ' ')

            if servidor.campus:
                doc.append(NoEscape(r'($\times$) CAMPUS DE: '))
                doc.append(servidor.campus)
            else:
                doc.append(NoEscape(r'() CAMPUS DE: '))
            doc.append(NewLine())

            doc.append(NoEscape('E-mail: '))
            doc.append(escape_latex(servidor.email))
            doc.append(NewLine())

            doc.append('Telefone: ')
            doc.append(servidor.telefone)
            doc.append(NewLine())

            doc.append('Endereço: ')
            doc.append(servidor.logradouro + ', ' + servidor.cidade + ', ' + servidor.estado)
            doc.append(NewLine())

            with doc.create(MdFramed(options=mdframed_options)):
                doc.append('Função: ')
                doc.append(NewLine())
                tabela_alternativas(doc, FuncaoServidor, 'XXX',
                             id=servidor_cursoextensao.funcao.id, hline=False)

            doc.append(NoEscape(r'\bigskip'))
            doc.append(NoEscape(r'\bigskip'))
            doc.append(NoEscape(r'Assinatura do participante: \hrulefill \\ \\ \\'))
            doc.append(NoEscape(r'Assinatura da chefia imediata: \hrulefill \\ \\'))

            doc.append(bold('PLANO DE TRABALHO: '))
            doc.append(escape_latex(servidor_cursoextensao.plano_trabalho))


def mdframed_plano_trabalho(doc, models):
    doc.append(LineBreak())

    mdframed_options_plano = 'innertopmargin=5pt, innerleftmargin=3pt, innerrightmargin=3pt, topline=false'

    with doc.create(MdFramed(options=mdframed_options_plano)):
        doc.append(bold('PLANO DE TRABALHO: '))

        planos = []
        for model in models:
            planos.append(model.plano_trabalho)

        for plano in planos:
            doc.append(escape_latex(plano))
            doc.append(NewLine())


def tabela_discentes(doc, enum, projeto_extensao):
    table_spec = NoEscape(r'''>{\centering\arraybackslash}X|
                          @{    }c@{    }|
                          @{    }c@{    }|
                          @{    }c@{    }|
                          @{    }c@{    }|
                          >{\centering\arraybackslash}X|
                          ''')
    cabecalho = ['NOME COMPLETO',
                 'CURSO',
                 'SÉRIE',
                 'TURNO',
                 'C/H SEMANAL',
                 'TELEFONE E E-MAIL']

    doc.append(NoEscape('{\scriptsize'))

    with doc.create(Tabularx('|' + table_spec, width_argument=width_argument)) as tab:
        tab.add_hline()
        tab.add_row(cabecalho)
        tab.add_hline()

        discentes = Discente_CursoExtensao.objects.filter(curso_extensao=projeto_extensao.id)
        for discente in discentes:
            linha = [discente.nome,
                     discente.curso,
                     discente.serie,
                     discente.turno.nome,
                     discente.carga_horaria_semanal,
                     NoEscape(discente.telefone + ', \n' + '\leavevmode\hspace{0pt}' + escape_latex(discente.email))]
            tab.add_row(linha)
            tab.add_hline()

    mdframed_plano_trabalho(doc, discentes)

    doc.append(NoEscape('}')) # volta com tamanho da fonte normal


def tabela_membros(doc, enum, projeto_extensao):
    table_spec = NoEscape(r'''@{    }c@{    }|
                          >{\centering\arraybackslash}X|
                          @{    }c@{    }|
                          @{    }c@{    }|
                          @{    }c@{    }|
                          >{\centering\arraybackslash}X|
                          >{\centering\arraybackslash}X|
                          ''')
    cabecalho = ['NOME COMPLETO',
                 'INSTITUIÇÃO/ ENTIDADE',
                 'CPF',
                 'DATA DE NASC.',
                 'FUNÇÃO',
                 'C/H SEMANAL',
                 'TELEFONE E E-MAIL']

    doc.append(NoEscape('{\scriptsize'))

    with doc.create(Tabularx('|' + table_spec, width_argument=width_argument)) as tab:
        tab.add_hline()
        tab.add_row(cabecalho)
        tab.add_hline()

        membros = MembroComunidade_CursoExtensao.objects.filter(curso_extensao=projeto_extensao.id)
        for membro in membros:
            linha = [membro.nome,
                     membro.entidade,
                     membro.cpf,
                     str(membro.data_nascimento),
                     membro.funcao,
                     membro.carga_horaria_semanal,
                     NoEscape(membro.telefone + ', \n' + '\leavevmode\hspace{0pt}' + escape_latex(membro.email))]
            tab.add_row(linha)
            tab.add_hline()

    mdframed_plano_trabalho(doc, membros)

    doc.append(NoEscape('}')) # volta com tamanho da fonte normal


def tabela_previsao_orcamentaria(doc, enum, previsao_orcamentaria):
        item(doc, enum, 'PREVISÃO ORÇAMENTÁRIA: ')
        doc.append(NewLine())

        total_receitas = (previsao_orcamentaria.inscricoes +
            previsao_orcamentaria.convenios +
            previsao_orcamentaria.patrocinios +
            previsao_orcamentaria.fonte_financiamento)

        total_despesas = (previsao_orcamentaria.honorarios +
            previsao_orcamentaria.passagens +
            previsao_orcamentaria.alimentacao +
            previsao_orcamentaria.hospedagem +
            previsao_orcamentaria.divulgacao +
            previsao_orcamentaria.material_consumo +
            previsao_orcamentaria.xerox +
            previsao_orcamentaria.certificados +
            previsao_orcamentaria.outros)

        with doc.create(Tabularx('|' + 'X|'*4, width_argument=width_argument)) as tab:
            tab.add_hline()
            tab.add_row(MultiColumn(2, data=bold('Receitas'), align='|c|'),
                        MultiColumn(2, data=bold('Despesas'), align='c|'))
            tab.add_hline()
            tab.add_row('Inscrições', previsao_orcamentaria.inscricoes,
                        'Honorários', previsao_orcamentaria.honorarios)
            tab.add_hline()
            tab.add_row('Convênios', previsao_orcamentaria.convenios,
                        'Passagens', previsao_orcamentaria.passagens)
            tab.add_hline()
            tab.add_row('Patrocínios', previsao_orcamentaria.patrocinios,
                        'Alimentação', previsao_orcamentaria.alimentacao)
            tab.add_hline()
            tab.add_row('Fonte(s) de financiamento', previsao_orcamentaria.fonte_financiamento,
                        'Hospedagem', previsao_orcamentaria.hospedagem)
            tab.add_hline()
            tab.add_row('', '',
                        'Divulgação', previsao_orcamentaria.divulgacao)
            tab.add_hline()
            tab.add_row('', '',
                        'Material de consumo', previsao_orcamentaria.material_consumo)
            tab.add_hline()
            tab.add_row('', '',
                        'Xerox', previsao_orcamentaria.xerox)
            tab.add_hline()
            tab.add_row('', '',
                        'Certificados', previsao_orcamentaria.certificados)
            tab.add_hline()
            tab.add_row('', '',
                        'Outros (especificar)', str(previsao_orcamentaria.outros) + '\n' + \
                        previsao_orcamentaria.outros_especificacao)
            tab.add_hline()
            tab.add_row(bold('Total'), total_receitas,
                        MultiRow(2, data=bold('Total')), MultiRow(2, data=total_despesas))
            doc.append(NoEscape('\cline{1-2}'))
            # TODO: não tem atributo para saldo previsto na classe PrevisaoOrcamentara
            tab.add_row(bold('Saldo previsto'), '', '', '')
            tab.add_hline()


def tabela_gestao_recursos_financeiros(doc, enum, previsao_orcamentaria):
        item(doc, enum, 'GESTÃO DOS RECURSOS FINANCEIROS: ')
        doc.append(NewLine())

        with doc.create(MdFramed(options=mdframed_options)):
            doc.append(bold('ÓRGÃO GESTOR DOS RECURSOS FINANCEIROS '))
            doc.append(NewLine())

            doc.append(NoEscape(r'IDENTIFICAÇÃO: \\'))

            for tipo_gestao in TipoGestaoRecursosFinanceiros.objects.all():
                if previsao_orcamentaria.identificacao and previsao_orcamentaria.identificacao.id == tipo_gestao.id:
                    doc.append(NoEscape(r'($\times$) ' + tipo_gestao.nome.upper()))
                else:
                    doc.append(('() ' + tipo_gestao.nome.upper()))
                doc.append(NewLine())


# Relatórios
def tabela_certificados(doc, id=None):
    with doc.create(Enumerate()) as enum:
        enum.add_item('Relacionar o nome dos participantes com direito a certificados.')
        doc.append(NewLine())
        table_spec = NoEscape(r'''>{\centering\arraybackslash}X|
                              @{    }c@{    }|
                              @{    }c@{    }|
                              @{    }c@{    }|
                              ''')
        cabecalho = ['NOME',
                     'FUNÇÃO',
                     'FREQUÊNCIA (%)',
                     'C/H TOTAL']

        with doc.create(Tabularx('|' + table_spec, width_argument=width_argument)) as tab:
            tab.add_hline()
            tab.add_row(cabecalho)
            tab.add_hline()

            # TODO: teste
            #  certificado = CertificadoRelatorio.objects.filter(relatorio_id=id)
            certificados = CertificadoRelatorio.objects.all()
            for certificado in certificados:
                linha = [certificado.nome,
                         certificado.funcao,
                         certificado.frequencia,
                         certificado.carga_horaria_total]
                tab.add_row(linha)
                tab.add_hline()

        doc.append(LineBreak())

        # TODO: Item 9.2: Inserir onde o certificado sera gerado: PROEX ou Centro de Coordenação / Órgão Promotor
        enum.add_item(NoEscape(r'Informar se os certificados devem ser emitidos: \\'))
        doc.append(NoEscape('() pela PROEX \hfill () pelo Centro da Coordenação ou Órgão Promotor'))


def local_data_assinatura(doc):
    doc.append(NoEscape(r'\raggedleft'))
    doc.append(NoEscape(r'\bigskip'))
    with doc.create(MiniPage(width=r'.5\textwidth')):
        center = Center()
        center.append(NoEscape('\hrulefill'))
        center.append(NewLine())
        center.append(NoEscape(r'\bigskip'))
        center.append(NoEscape(r'Local e data \\'))
        center.append(NoEscape('\hrulefill'))
        center.append(NewLine())
        center.append(NoEscape(r'\bigskip'))
        center.append(NoEscape('Assinatura do(a) Coordenador(a) da Atividade'))
        doc.append(center)
