from pylatex import NoEscape, FlushRight, NewLine, MdFramed, Enumerate, Document, \
     NewPage, HFill, Tabularx, LineBreak, MultiColumn, MultiRow
from pylatex.utils import escape_latex, bold

from base.models import *
from curso_extensao.models import *


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


def cabecalho(doc):
    cabecalho = r'''
\renewcommand{\headrulewidth}{0pt}%
\renewcommand{\footrulewidth}{0pt}%
\fancyhead[L]{%
    \includegraphics[width=200px]{./img/logo_unioeste.png}
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
    \includegraphics[width=80px]{./img/logo_governo.jpg}
}
    '''

    doc.append(NoEscape(cabecalho))


def rodape(doc, texto):
    rodape = r'''
\fancyfoot[R]{
    {\footnotesize \texttt{%(texto)s}}
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
    \includegraphics[width=100px]{./img/logo_extensao.jpg}
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


def mdframed_informar(doc, enum, projeto_extensao):
    with doc.create(MdFramed(options=mdframed_options)):
        item(doc, enum, 'INFORMAR: ')
        with doc.create(Enumerate()) as subenum:
            doc.append(NoEscape('\scriptsize'))

            subenum.add_item(NoEscape('Esta atividade faz parte de algum Programa de Extensão? '))
            if projeto_extensao.programa_extensao:
                doc.append(NoEscape(r'Não () Sim ({$\times$}): Qual? '))
                doc.append(projeto_extensao.programa_extensao.nome)
            else:
                doc.append(NoEscape(r'Não ($\times$) Sim (): Qual? '))

            doc.append(NoEscape(r'''
            Coordenador(a) do Programa: \\ \\ \\
            Assinatura: \hrulefill \\
            '''))

            # TODO: ???
            subenum.add_item('Esta Atividade de Extensão está articulada (quando for o caso): ao Ensino () à Pesquisa ()')


def tabela_unidade_administrativa(doc, enum, projeto_extensao):
        item(doc, enum, 'UNIDADE ADMINISTRATIVA: ')
        for ua in UnidadeAdministrativa.objects.all():
            if projeto_extensao.unidade_administrativa and projeto_extensao.unidade_administrativa.id == ua.id:
                doc.append(NoEscape(ua.nome + r' ($\times$) '))
            else:
                doc.append(ua.nome + ' () ')
        doc.append(NewLine())

        doc.append(bold('CAMPUS DE: '))
        for campus in Campus.objects.all():
            if projeto_extensao.campus and projeto_extensao.campus.id == campus.id:
                doc.append(NoEscape(campus.nome + r' ($\times$) '))
            else:
                doc.append(campus.nome + ' () ')


def tabela_centro(doc, enum, projeto_extensao):
    item(doc, enum, 'CENTRO: ')
    doc.append(NewLine())
    for centro in Centro.objects.all():
        if projeto_extensao.centro and projeto_extensao.centro.id == centro.id:
            doc.append(NoEscape(centro.nome + r' ($\times$) '))
        else:
            doc.append(centro.nome + ' () ')


# id é opcional, só se quiser preencher a tabela
def tabela_alternativas(doc, model, table_spec, id=None, hline=True):
    from pylatex import Tabularx, NoEscape

    # Conta a quantidade de 'X', 'l', 'c', 'r' etc.
    nro_colunas = sum(char.isalpha() for char in table_spec)

    with doc.create(Tabularx(table_spec, width_argument=NoEscape('\linewidth'))) as tab:
        if hline: tab.add_hline()
        row = []
        for i, obj in enumerate(model.objects.all(), 1):
            if id and obj.id == id:
                row.append(NoEscape(r'($\times$) ' + obj.nome))
            else:
                row.append('() ' + obj.nome)

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
    #  if projeto_extensao.grande_area:
    tabela_alternativas(doc, GrandeArea, '|X|X|X|', id=id)


def tabela_palavras_chave(doc, enum):
    item(doc, enum, 'PALAVRAS-CHAVE: ')
    doc.append(NewLine())
    tabela_alternativas(doc, PalavraChave_CursoExtensao, '|X|X|X|')


def tabela_area_tematica_principal(doc, enum, projeto_extensao, id):
    item(doc, enum, 'ÁREA TEMÁTICA PRINCIPAL: ')
    doc.append(NewLine())
    if projeto_extensao.area_tematica_principal:
        tabela_alternativas(doc, AreaTematica, '|X|X|X|', id=id)


def tabela_area_tematica_secundaria(doc, enum, projeto_extensao, id):
    item(doc, enum, 'ÁREA TEMÁTICA SECUNDÁRIA: ')
    doc.append(NewLine())
    if projeto_extensao.area_tematica_secundaria:
        tabela_alternativas(doc, AreaTematica, '|X|X|X|', id=id)
    else:
        tabela_alternativas(doc, AreaTematica, '|X|X|X|')


def tabela_linha_extensao(doc, enum, projeto_extensao, id):
    doc.append(NewPage())
    item(doc, enum, 'LINHA DE EXTENSÃO: ')
    doc.append(NewLine())
    doc.append(NewLine())
    doc.append(NoEscape(r'{\tiny'))
    if projeto_extensao.linha_extensao:
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

            # TODO: \linebreak aqui pra dar espaço pra assinatura
            doc.append(NoEscape(r'Assinatura do participante: \hrulefill \\ \\'))
            doc.append(NoEscape(r'Assinatura da chefia imediata: \hrulefill \\ \\'))

            doc.append(bold('PLANO DE TRABALHO: '))
            doc.append(escape_latex(servidor_cursoextensao.plano_trabalho))


def mdframed_plano_trabalho(doc, models):
    doc.append(LineBreak())

    mdframed_options_plano = 'innertopmargin=5pt, innerleftmargin=3pt, innerrightmargin=3pt, topline=false'

    with doc.create(MdFramed(options=mdframed_options_plano)):
        doc.append(bold('PLANO DE TRABALHO: '))

        planos = []
        for obj in models:
            planos.append(obj.plano_trabalho)

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
                        'Outros (especificar)', str(previsao_orcamentaria.outros) + '\n' + previsao_orcamentaria.outros_especificacao)
            tab.add_hline()
            tab.add_row(bold('Total'), total_receitas,
                        MultiRow(2, data=NoEscape(r'\hfill \textbf{Total}')), total_despesas)
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

            for obj in TipoGestaoRecursosFinanceiros.objects.all():
                if previsao_orcamentaria.identificacao and previsao_orcamentaria.identificacao.id == obj.id:
                    doc.append(NoEscape(r'($\times$) ' + obj.nome.upper()))
                else:
                    doc.append(('() ' + obj.nome.upper()))
                doc.append(NewLine())
