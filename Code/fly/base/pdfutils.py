# -*- coding: utf-8 -*-

from pylatex import NoEscape, FlushRight, NewLine, MdFramed, Enumerate, Document, NewPage, HFill, \
     Tabularx, LineBreak, MultiColumn, MultiRow, Package, Center, MiniPage
from pylatex.utils import escape_latex, bold

from base.models import *
from curso_extensao.models import *
from docente.models import *
from relatorio.models import *
from fly.settings import BASE_DIR


TIMES = NoEscape(r'\ding{53}')
PHANTOM = NoEscape(r'\phantom{\ding{53}}')

WIDTH_ARGUMENT = NoEscape(r'\linewidth')
MDFRAMED_OPTIONS = ['innertopmargin=5pt, innerleftmargin=3pt, innerrightmargin=3pt']

COMPILER = 'latexmk'
COMPILER_ARGS = ['-lualatex', '-verbose']


def init_document():
    geometry_options = {'left': '3cm',
                        'right': '1.5cm',
                        'bottom': '2.5cm',
                        'top': '6.5cm',
                        'headheight': '4cm'}
    doc = Document(geometry_options=geometry_options, lmodern=False, document_options=['12pt', 'a4paper', 'oneside', 'brazil'])

    return doc


def pacotes(doc):
    doc.packages.add(Package('microtype'))
    doc.packages.add(Package('indentfirst'))
    doc.packages.add(Package('graphicx'))
    doc.packages.add(Package('float'))
    doc.packages.add(Package('titlesec'))
    doc.packages.add(Package('parskip'))
    doc.packages.add(Package('enumitem'))
    # doc.packages.add(Package('helvet', options='scaled=0.92'))
    doc.packages.add(Package('tabularx'))
    doc.packages.add(Package('mdframed'))
    doc.packages.add(Package('eqparbox')) # similar a minipage
    doc.packages.add(Package('fancyhdr')) # cabeçalho?
    doc.packages.add(Package('makecell')) # criação de células em tabelas
    doc.packages.add(Package('calc')) # \widthof
    doc.packages.add(Package('fontspec')) # para fonte TeX Gyre Heros ('ª' e 'º' não funcionam com helvet)
    doc.packages.add(Package('pifont')) # \ding
    doc.packages.add(Package('csquotes')) # \MakeOuterQuote


def configuracoes_preambulo(doc):
    # doc.preamble.append(NoEscape(r'\renewcommand{\familydefault}{\sfdefault}'))
    # doc.append(NoEscape(r'\fontfamily{\sfdefault}\selectfont'))
    doc.preamble.append(NoEscape(r'\setmainfont[Scale=0.9]{TeX Gyre Heros}')) # fonte parecida com Arial e Helvetica

    doc.preamble.append(NoEscape(r'\MakeOuterQuote{"}')) # coverte aspas automaticamente, sem precisar de `` e ''

    # Configuração das listas
    doc.preamble.append(NoEscape(r'''
\setlist[enumerate, 1]{label*=\textbf{\arabic*}, leftmargin=*}
\setlist[enumerate, 2]{label*=\textbf{.\arabic*}, leftmargin=*}
    '''))

    # Configuração dos cabeçalhos
    doc.preamble.append(NoEscape('\pagestyle{fancy}'))

    # Diretório das imagens
    diretorio_img = '{}/base/static/img/'.format(BASE_DIR) # necessário barra no final
    doc.preamble.append(NoEscape(r'\graphicspath{{' + diretorio_img + '}}'))

    # Tamanho da fonte
    doc.append(NoEscape(r'\footnotesize'))


def cabecalho(doc):
    doc.append(NoEscape(r'''
\renewcommand{\headrulewidth}{0pt}%
\renewcommand{\footrulewidth}{0pt}%
\fancyhead[L]{%
    \includegraphics[width=200px]{logo_unioeste.png}
    \newline
    {\footnotesize
        Reitoria -- CNPJ 78680337/0001-84 \\
        Rua Universitária, 1619 -- Fone: (45) 3220-3000 -- Fax: (45) 3324-4590 \\
        Jardim Universitário -- Cx. P. 000701 -- CEP 85819-110 -- Cascavel -- Paraná \\
        www.unioeste.br
    }
}
\fancyhead[R]{%
    \includegraphics[width=80px]{logo_governo.jpg}
}
    '''))


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
    \includegraphics[width=100px]{logo_extensao_menor.jpg}
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
    with doc.create(MdFramed(options=MDFRAMED_OPTIONS)):
        item(doc, enum, 'INFORMAR: ')
        with doc.create(Enumerate()) as subenum:
            doc.append(NoEscape('\scriptsize'))

            subenum.add_item(NoEscape('Esta atividade faz parte de algum Programa de Extensão? '))
            if programa_extensao:
                doc.append(NoEscape(r'Não ({}) Sim ({}): Qual? {}'.format(PHANTOM, TIMES, programa_extensao.nome)))
            else:
                doc.append(NoEscape(r'Não ({}) Sim ({}): Qual? '.format(TIMES, PHANTOM)))

            doc.append(NoEscape(r'''
Coordenador(a) do Programa: \\ \\ \\
Assinatura: \hrulefill \\
            '''))

            # TODO: ???
            subenum.add_item(NoEscape(r'\
                                      Esta Atividade de Extensão está articulada (quando for o caso): \
                                      ao Ensino ({}) à Pesquisa ({})'.format(PHANTOM, PHANTOM)))


def tabela_unidade_administrativa(doc, enum, unidade_administrativa, campus):
        item(doc, enum, 'UNIDADE ADMINISTRATIVA: ')
        for unidade in UnidadeAdministrativa.objects.all():
            if unidade_administrativa and unidade_administrativa.id == unidade.id:
                doc.append(NoEscape(r'{} ({}) '.format(unidade.nome, TIMES)))
            else:
                doc.append(NoEscape(r'{} ({}) '.format(unidade.nome, PHANTOM)))
        doc.append(NewLine())

        doc.append(bold('CAMPUS DE: '))
        for c in Campus.objects.all():
            if campus and campus.id == c.id:
                doc.append(NoEscape(r'{} ({}) '.format(c.nome, TIMES)))
            else:
                doc.append(NoEscape(r'{} ({}) '.format(c.nome, PHANTOM)))


def tabela_centro(doc, enum, centro):
    item(doc, enum, 'CENTRO: ')
    doc.append(NewLine())
    for c in Centro.objects.all():
        if centro and centro.id == c.id:
            doc.append(NoEscape(r'{} ({}) '.format(c.nome, TIMES)))
        else:
            doc.append(NoEscape(r'{} ({}) '.format(c.nome, PHANTOM)))


# id é opcional, só se quiser preencher a tabela
def tabela_alternativas(doc, model, table_spec, id=None, hline=True):
    from pylatex import Tabularx, NoEscape

    # Conta a quantidade de 'X', 'l', 'c', 'r' etc.
    nro_colunas = sum(char.isalpha() for char in table_spec)

    with doc.create(Tabularx(table_spec, width_argument=WIDTH_ARGUMENT)) as tab:
        if hline:
            tab.add_hline()

        row = []
        for i, model in enumerate(model.objects.all(), 1):
            if id and model.id == id:
                row.append(NoEscape(r'({}) {}'.format(TIMES, model.nome)))
            else:
                row.append(NoEscape(r'({}) {} '.format(PHANTOM, model.nome)))

            if i%nro_colunas == 0:
                tab.add_row(row)
                del row[:]

        # Adiciona o resto dos itens à tabela
        if len(row):
            for _ in range(nro_colunas - len(row)):
                row.append('')
            tab.add_row(row, strict=False)

        if hline: tab.add_hline()


def tabela_grande_area(doc, enum, id=None):
    item(doc, enum, 'GRANDE ÁREA: ')
    doc.append(NewLine())
    tabela_alternativas(doc, GrandeArea, '|X|X|X|', id=id)


def tabela_palavras_chave(doc, enum, palavras):
    item(doc, enum, 'PALAVRAS-CHAVE: ')
    doc.append(NewLine())

    nro_colunas = 3
    with doc.create(Tabularx('|X|X|X|', width_argument=WIDTH_ARGUMENT)) as tab:
        tab.add_hline()

        row = []
        for i, palavra in enumerate(palavras, 1):
            row.append(NoEscape('{} -- {}'.format(str(i), escape_latex(palavra.nome))))

            if i%nro_colunas == 0:
                tab.add_row(row)
                del row[:]

        # Adiciona o resto dos itens à tabela
        for _ in range(nro_colunas - len(row)):
            row.append('')
        tab.add_row(row)

        tab.add_hline()


def tabela_area_tematica_principal(doc, enum, id):
    item(doc, enum, 'ÁREA TEMÁTICA PRINCIPAL: ')
    doc.append(NewLine())
    tabela_alternativas(doc, AreaTematica, '|X|X|X|', id=id)


def tabela_area_tematica_secundaria(doc, enum, area_tematica_secundaria, id=None):
    item(doc, enum, 'ÁREA TEMÁTICA SECUNDÁRIA: ')
    doc.append(NewLine())
    tabela_alternativas(doc, AreaTematica, '|X|X|X|', id=id)


def tabela_linha_extensao(doc, enum, linha_extensao, id):
    doc.append(NewPage())
    item(doc, enum, 'LINHA DE EXTENSÃO: ')
    doc.append(NewLine())
    doc.append(NewLine())
    doc.append(NoEscape(r'{\scriptsize'))
    if linha_extensao:
        tabela_alternativas(doc, LinhaExtensao, 'X|X|X', id=id, hline=False)
    doc.append(NoEscape('}'))


def popular_servidores(doc, servidor, docente_cursoextensao=None):
    with doc.create(MdFramed(options=MDFRAMED_OPTIONS)):
        doc.append(bold('SERVIDORES UNIOESTE '))
        doc.append(NewLine())

        doc.append(NoEscape('Nome completo: '))
        doc.append(escape_latex(servidor.nome_completo))
        doc.append(NewLine())

        if servidor.__class__ == Docente_CursoExtensao:
            for tipo_docente in TipoDocente.objects.all():
                if docente.tipo_docente.id == tipo_docente.id:
                    doc.append(NoEscape(r'({}) {} '.format(TIMES, tipo_docente.nome)))
                else:
                    doc.append(NoEscape(r'({}) {} '.format(PHANTOM, tipo_docente.nome)))
            doc.append(NoEscape(r'({}) {} '.format(PHANTOM, 'Agente Universitário')))
            doc.append(NewLine())
        elif servidor.__class__ == AgenteUniversitario_CursoExtensao:
            for tipo_docente in TipoDocente.objects.all():
                doc.append(NoEscape(r'({}) {} '.format(PHANTOM, tipo_docente.nome)))
            doc.append(NoEscape(r'({}) {} '.format(TIMES, 'Agente Universitário')))
            doc.append(NewLine())

        # TODO: regime_trabalho
        #  doc.append('Regime de trabalho: ')
        #  doc.append(servidor.regime_trabalho)
        #  doc.append(NoEscape('\ hora(s) \hfill'))

        doc.append('Carga horária semanal dedicada à atividade: ')
        if docente_cursoextensao:
            doc.append(docente_cursoextensao.carga_horaria_dedicada)
        else:
            doc.append(servidor.carga_horaria_dedicada)
        doc.append(NoEscape('\ hora(s) \hfill'))
        doc.append(NewLine())

        doc.append('Colegiado: ')
        doc.append(escape_latex(servidor.colegiado))
        doc.append(NewLine())

        doc.append('Centro: ')
        doc.append(servidor.centro.nome)
        doc.append(NewLine())

        # TODO: unidade_administrativa
        #  doc.append('Unidade Administrativa: ')
        #  for unidade in UnidadeAdministrativa.objects.all():
        #      if agente_cursoextensao.unidade_administrativa and agente_cursoextensao.unidade_administrativa.id == unidade.id:
        #          doc.append(NoEscape(r'({}) {} '.format(TIMES, unidade.nome)))
        #      else:
        #          doc.append(NoEscape(r'({}) {} '.format(PHANTOM, unidade.nome)))

        #  if agente_cursoextensao.campus:
        #      doc.append(NoEscape(r'({}) CAMPUS DE: {}'.format(TIMES, agente_cursoextensao.campus.nome)))
        #  else:
        #      doc.append(NoEscape(r'({}) CAMPUS DE: '.format(PHANTOM)))
        #  doc.append(NewLine())

        doc.append(NoEscape('E-mail: '))
        doc.append(escape_latex(servidor.email))
        doc.append(NewLine())

        doc.append('Telefone: ')
        doc.append(escape_latex(servidor.telefone))
        doc.append(NewLine())

        doc.append('Endereço: ')
        doc.append(NoEscape('{}, {} -- {} -- {}'.format(escape_latex(servidor.logradouro),
                                                        escape_latex(servidor.cidade),
                                                        escape_latex(servidor.estado),
                                                        escape_latex(servidor.pais))))
        doc.append(NewLine())

        with doc.create(MdFramed(options=MDFRAMED_OPTIONS)):
            doc.append('Função: ')
            doc.append(NewLine())
            if docente_cursoextensao:
                tabela_alternativas(doc, FuncaoServidor, 'XXX',
                                    id=docente_cursoextensao.funcao.id, hline=False)
            else:
                tabela_alternativas(doc, FuncaoServidor, 'XXX',
                                    id=servidor.funcao.id, hline=False)

        doc.append(NoEscape(r'\bigskip'))
        doc.append(NoEscape(r'\bigskip'))
        doc.append(NoEscape(r'Assinatura do participante: \hrulefill \\ \\ \\'))
        doc.append(NoEscape(r'Assinatura da chefia imediata: \hrulefill \\ \\'))

        doc.append(bold('PLANO DE TRABALHO: '))
        if docente_cursoextensao:
            doc.append(escape_latex(docente_cursoextensao.plano_trabalho))
        else:
            doc.append(escape_latex(servidor.plano_trabalho))


def mdframed_equipe_trabalho(doc, enum, projeto_extensao):
    # itera sobre os docentes
    docentes_cursoextensao = Docente_CursoExtensao.objects.filter(curso_extensao_id=projeto_extensao.id)
    for docente_cursoextensao in docentes_cursoextensao:
        docente = docente_cursoextensao.docente
        popular_servidores(doc, docente, docente_cursoextensao)

    # itera sobre os agentes universitários
    agentes_cursoextensao = AgenteUniversitario_CursoExtensao.objects.filter(curso_extensao_id=projeto_extensao.id)
    for agente_cursoextensao in agentes_cursoextensao:
        popular_servidores(doc, agente_cursoextensao)


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
    table_spec = NoEscape(r'''|>{\centering\arraybackslash}X|
                              >{\centering\arraybackslash}X|
                              @{  }c@{  }|
                              @{  }c@{  }|
                              >{\centering\arraybackslash}X|
                              @{  }c@{  }|
                          ''')
    cabecalho = ['NOME COMPLETO',
                 'CURSO',
                 'SÉRIE',
                 'TURNO',
                 'C/H SEMANAL',
                 'TELEFONE E E-MAIL']

    doc.append(NoEscape('{\scriptsize'))

    with doc.create(Tabularx(table_spec, width_argument=WIDTH_ARGUMENT)) as tab:
        tab.add_hline()
        tab.add_row(cabecalho)
        tab.add_hline()

        discentes = Discente_CursoExtensao.objects.filter(curso_extensao_id=projeto_extensao.id)
        for discente in discentes:
            linha = [
                escape_latex(discente.nome),
                escape_latex(discente.curso.nome),
                discente.serie,
                discente.turno.nome,
                discente.carga_horaria_semanal,
                # TODO: hifenizar email
                NoEscape(r'\makecell{{ {}; \\ {} }}'.format(escape_latex(discente.telefone),
                                                            escape_latex(discente.email)))
            ]
            tab.add_row(linha)
            tab.add_hline()

    mdframed_plano_trabalho(doc, discentes)

    doc.append(NoEscape('}')) # volta com tamanho normal da fonte


def tabela_membros(doc, enum, projeto_extensao):
    table_spec = NoEscape(r'''|>{\centering\arraybackslash}X|
                              >{\centering\arraybackslash}X|
                              @{  }c@{  }|
                              @{  }c@{  }|
                              >{\centering\arraybackslash}X|
                              >{\centering\arraybackslash}X|
                              @{  }c@{  }|
                          ''')
    cabecalho = ['NOME COMPLETO',
                 'ENTIDADE',
                 'CPF',
                 'DATA NASC.',
                 'FUNÇÃO',
                 'C/H SEMANAL',
                 'TELEFONE E E-MAIL']

    doc.append(NoEscape('{\scriptsize'))

    with doc.create(Tabularx(table_spec, width_argument=WIDTH_ARGUMENT)) as tab:
        tab.add_hline()
        tab.add_row(cabecalho)
        tab.add_hline()

        membros = MembroComunidade_CursoExtensao.objects.filter(curso_extensao_id=projeto_extensao.id)
        for membro in membros:
            linha = [
                escape_latex(membro.nome),
                escape_latex(membro.entidade),
                escape_latex(membro.cpf),
                membro.data_nascimento.strftime('%d/%m/%Y'),
                escape_latex(membro.funcao),
                membro.carga_horaria_semanal,
                # TODO: hifenizar email
                NoEscape(r'\makecell{{ {}; \\ {} }}'.format(escape_latex(membro.telefone),
                                                            escape_latex(membro.email)))
            ]
            tab.add_row(linha)
            tab.add_hline()

    mdframed_plano_trabalho(doc, membros)

    doc.append(NoEscape('}')) # volta com tamanho da fonte normal


# TODO: juntar a tabela_discentes e a tabela_membros nessa
def tabela_discentes_membros(doc, enum, projeto_extensao):
    pass


def tabela_previsao_orcamentaria(doc, enum, previsao_orcamentaria):
        item(doc, enum, 'PREVISÃO ORÇAMENTÁRIA: ')
        doc.append(NewLine())

        # TODO: blank=True para os DecimalField
        inscricoes           = previsao_orcamentaria.inscricoes           or 0
        convenios            = previsao_orcamentaria.convenios            or 0
        patrocinios          = previsao_orcamentaria.patrocinios          or 0
        fonte_financiamento  = previsao_orcamentaria.fonte_financiamento  or 0
        honorarios           = previsao_orcamentaria.honorarios           or 0
        passagens            = previsao_orcamentaria.passagens            or 0
        alimentacao          = previsao_orcamentaria.alimentacao          or 0
        hospedagem           = previsao_orcamentaria.hospedagem           or 0
        divulgacao           = previsao_orcamentaria.divulgacao           or 0
        material_consumo     = previsao_orcamentaria.material_consumo     or 0
        xerox                = previsao_orcamentaria.xerox                or 0
        certificados         = previsao_orcamentaria.certificados         or 0
        outros               = previsao_orcamentaria.outros               or 0
        outros_especificacao = previsao_orcamentaria.outros_especificacao or ''
        fundacao             = previsao_orcamentaria.fundacao             or ''
        outro_orgao_gestor   = previsao_orcamentaria.outro_orgao_gestor   or ''

        total_receitas = (inscricoes +
                          convenios +
                          patrocinios +
                          fonte_financiamento)

        total_despesas = (honorarios +
                          passagens +
                          alimentacao +
                          hospedagem +
                          divulgacao +
                          material_consumo +
                          xerox +
                          certificados +
                          outros)

        with doc.create(Tabularx('|' + 'X|'*4, width_argument=WIDTH_ARGUMENT)) as tab:
            tab.add_hline()

            tab.add_row(MultiColumn(2, data=bold('Receitas'), align='|c|'),
                        MultiColumn(2, data=bold('Despesas'), align='c|'))
            tab.add_hline()

            tab.add_row('Inscrições', inscricoes,
                        'Honorários', honorarios)
            tab.add_hline()

            tab.add_row('Convênios', convenios,
                        'Passagens', passagens)
            tab.add_hline()

            tab.add_row('Patrocínios', patrocinios,
                        'Alimentação', alimentacao)
            tab.add_hline()

            tab.add_row('Fonte(s) de financiamento', fonte_financiamento,
                        'Hospedagem', hospedagem)
            tab.add_hline()

            tab.add_row('', '',
                        'Divulgação', divulgacao)
            tab.add_hline()

            tab.add_row('', '',
                        'Material de consumo', material_consumo)
            tab.add_hline()

            tab.add_row('', '',
                        'Xerox', xerox)
            tab.add_hline()

            tab.add_row('', '',
                        'Certificados', certificados)
            tab.add_hline()

            tab.add_row('', '',
                        'Outros (especificar)', '{}\n{}'.format(str(outros), outros_especificacao))
            tab.add_hline()

            tab.add_row(bold('Total'), total_receitas,
                        MultiRow(2, data=bold('Total')), MultiRow(2, data=total_despesas))
            doc.append(NoEscape('\cline{1-2}'))

            # TODO: não tem atributo para saldo previsto na classe PrevisaoOrcamentaria_CursoExtensao
            tab.add_row(bold('Saldo previsto'), '', '', '')
            tab.add_hline()


def tabela_gestao_recursos_financeiros(doc, enum, previsao_orcamentaria):
        item(doc, enum, 'GESTÃO DOS RECURSOS FINANCEIROS: ')
        doc.append(NewLine())

        with doc.create(MdFramed(options=MDFRAMED_OPTIONS)):
            doc.append(bold('ÓRGÃO GESTOR DOS RECURSOS FINANCEIROS '))
            doc.append(NewLine())

            doc.append(NoEscape(r'IDENTIFICAÇÃO: \\'))

            for tipo_gestao in TipoGestaoRecursosFinanceiros.objects.all():
                if previsao_orcamentaria.identificacao and previsao_orcamentaria.identificacao.id == tipo_gestao.id:
                    doc.append(NoEscape(r'({}) {}'.format(TIMES, tipo_gestao.nome.upper())))
                else:
                    doc.append(NoEscape(r'({}) {}'.format(PHANTOM, tipo_gestao.nome.upper())))
                doc.append(NewLine())


# Relatórios
def tabela_certificados(doc, id=None):
    with doc.create(Enumerate()) as enum:
        enum.add_item('Relacionar o nome dos participantes com direito a certificados.')
        doc.append(NewLine())
        table_spec = NoEscape(r'''|>{\centering\arraybackslash}X|
                                  @{    }c@{    }|
                                  @{    }c@{    }|
                                  @{    }c@{    }|
                              ''')
        cabecalho = ['NOME',
                     'FUNÇÃO',
                     'FREQUÊNCIA (%)',
                     'C/H TOTAL']

        with doc.create(Tabularx(table_spec, width_argument=WIDTH_ARGUMENT)) as tab:
            tab.add_hline()
            tab.add_row(cabecalho)
            tab.add_hline()

            certificados = CertificadoRelatorio.objects.filter(relatorio_id=id)
            for certificado in certificados:
                if certificado:
                    linha = [escape_latex(certificado.nome),
                             certificado.funcao,
                             certificado.frequencia,
                             certificado.carga_horaria_total]
                    tab.add_row(linha)
                    tab.add_hline()

        doc.append(LineBreak())

        # TODO: Item 9.2: Inserir onde o certificado sera gerado: PROEX ou Centro de Coordenação / Órgão Promotor
        enum.add_item(NoEscape(r'Informar se os certificados devem ser emitidos: \\'))
        doc.append(NoEscape('({}) pela PROEX \hfill ({}) pelo Centro da Coordenação ou Órgão Promotor'.format(PHANTOM, PHANTOM)))


def local_data_assinatura(doc):
    doc.append(NoEscape(r'\raggedleft'))
    doc.append(NoEscape(r'\bigskip'))
    with doc.create(MiniPage(width=r'.5\textwidth')):
        center = Center()
        center.append(NoEscape('\hrulefill'))
        center.append(NewLine())
        center.append(NoEscape(r'\bigskip'))
        center.append(NoEscape(r'\bigskip'))
        center.append(NoEscape(r'Local e data \\'))
        center.append(NoEscape('\hrulefill'))
        center.append(NewLine())
        center.append(NoEscape(r'\bigskip'))
        center.append(NoEscape('Assinatura do(a) Coordenador(a) da Atividade'))
        doc.append(center)


# TODO: usar essa pra substituir a de cima
def assinatura(doc, texto, largura, pos_env):
    doc.append(NoEscape(r'\bigskip'))
    doc.append(NoEscape(r'\bigskip'))
    doc.append(NoEscape(r'\bigskip'))
    with doc.create(pos_env) as pos:
        with pos.create(MiniPage(width=largura)) as mini:
            mini.append(NoEscape('\hrulefill'))
            mini.append(NewLine())
            mini.append(NoEscape(r'{}'.format(texto)))
