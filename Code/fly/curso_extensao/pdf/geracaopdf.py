from pylatex import Document, Enumerate, NoEscape, Package, Tabularx, FlushRight, \
     LineBreak, NewLine, MultiColumn, MultiRow, HFill, Table
from pylatex.base_classes import Environment
from pylatex.frames import MdFramed
from pylatex.utils import escape_latex, bold

from base.models import *
from curso_extensao.models import *

mdframed_options = ['innertopmargin=5pt, innerleftmargin=3pt, innerrightmargin=3pt']
width_argument = NoEscape(r'\linewidth')

# id opcional, só se quiser preencher a tabela
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

def tabela_discentes_membros(doc, cabecalho, table_spec):
    from pylatex import Tabularx, NoEscape

    with doc.create(Tabularx('|' + table_spec, width_argument=width_argument)) as tab:
        tab.add_hline()
        tab.add_row(cabecalho)
        tab.add_hline()

        return tab

def formulario_previsao_orcamentaria(doc, enum, curso):
        enum.add_item(bold('PREVISÃO ORÇAMENTÁRIA: '))
        doc.append(NewLine())
        previsao_orcamentaria = PrevisaoOrcamentaria_CursoExtensao.objects.get(curso_extensao=curso.id)
        total_receitas = previsao_orcamentaria.inscricoes + \
            previsao_orcamentaria.convenios + \
            previsao_orcamentaria.patrocinios + \
            previsao_orcamentaria.fonte_financiamento
        total_despesas = previsao_orcamentaria.honorarios + \
            previsao_orcamentaria.passagens + \
            previsao_orcamentaria.alimentacao + \
            previsao_orcamentaria.hospedagem + \
            previsao_orcamentaria.divulgacao + \
            previsao_orcamentaria.material_consumo + \
            previsao_orcamentaria.xerox + \
            previsao_orcamentaria.certificados + \
            previsao_orcamentaria.outros

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

        enum.add_item(bold('GESTÃO DOS RECURSOS FINANCEIROS: '))
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

def item(doc, enum, texto, dado):
    enum.add_item(bold(texto))
    doc.append(escape_latex(dado))

def gerar_pdf(curso):
    # Pacotes e configurações
    geometry_options = {'tmargin': '2cm',
                        'bmargin': '2cm',
                        'lmargin': '2cm',
                        'rmargin': '1.5cm'}
    doc = Document(geometry_options=geometry_options,
            document_options=['12pt', 'a4paper', 'oneside'],
            lmodern=False)

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
    #  doc.packages.add(Package('hyphenat', options='none')) # impede hifenização

    doc.append(NoEscape(r'\fontfamily{\sfdefault}\selectfont'))

    # Configuração das listas
    doc.preamble.append(NoEscape(r'''
    \setlist[enumerate, 1]{label*=\textbf{\arabic*}, leftmargin=*}
    \setlist[enumerate, 2]{label*=\textbf{.\arabic*}, leftmargin=*}
    '''))

    # Início do documento
    flush_right = FlushRight()
    flush_right.append(NoEscape(r'FORMULÁRIO ESPECÍFICO PARA ATIVIDADES DE EXTENSÃO \\'))
    flush_right.append(NoEscape('MODALIDADE CURSO DE EXTENSÃO'))
    doc.append(flush_right)

    doc.append(NoEscape('\hrulefill'))

    with doc.create(Enumerate()) as enum:
        doc.append(NoEscape(r'\footnotesize'))

        item(doc, enum, 'TÍTULO: ', curso.titulo)

        item(doc, enum, 'COORDENADOR(a): ', curso.coordenador.nome_completo)

        periodo_realizacao = 'de ' + curso.periodo_realizacao_inicio.strftime('%d/%m/%Y') + ' a ' + curso.periodo_realizacao_fim.strftime('%d/%m/%Y')
        item(doc, enum, 'PERÍODO DE REALIZAÇÃO: ', periodo_realizacao)

        with doc.create(MdFramed(options=mdframed_options)):
            enum.add_item(bold('INFORMAR: '))
            with doc.create(Enumerate()) as subenum:
                doc.append(NoEscape('\scriptsize'))

                subenum.add_item(NoEscape('Esta atividade faz parte de algum Programa de Extensão? '))
                if curso.programa_extensao:
                    doc.append(NoEscape(r'Não () Sim ({$\times$}): Qual? '))
                    doc.append(curso.programa_extensao.nome)
                else:
                    doc.append(NoEscape(r'Não ($\times$) Sim (): Qual? '))

                doc.append(NoEscape(r'''
                Coordenador(a) do Programa: \\ \\ \\
                Assinatura: \hrulefill \\
                '''))
                # TODO: ???
                subenum.add_item('Esta Atividade de Extensão está articulada (quando for o caso): ao Ensino () à Pesquisa ()')

        enum.add_item(bold('UNIDADE ADMINISTRATIVA: '))
        for obj in UnidadeAdministrativa.objects.all():
            if curso.unidade_administrativa and curso.unidade_administrativa.id == obj.id:
                doc.append(NoEscape(obj.nome + r' ($\times$) '))
            else:
                doc.append(obj.nome + ' () ')
        doc.append(NewLine())

        doc.append(bold('CAMPUS DE: '))
        for obj in Campus.objects.all():
            if curso.campus and curso.campus.id == obj.id:
                doc.append(NoEscape(obj.nome + r' ($\times$) '))
            else:
                doc.append(obj.nome + ' () ')

        enum.add_item(bold('CENTRO: '))
        doc.append(NewLine())
        for obj in Centro.objects.all():
            if curso.centro and curso.centro.id == obj.id:
                doc.append(NoEscape(obj.nome + r' ($\times$) '))
            else:
                doc.append(obj.nome + ' () ')

        enum.add_item(bold('GRANDE ÁREA: '))
        doc.append(NewLine())
        if curso.grande_area:
            tabela_alternativas(doc, GrandeArea, '|X|X|X|', id=curso.grande_area.id)

        enum.add_item(bold('PALAVRAS-CHAVE: '))
        doc.append(NewLine())
        tabela_alternativas(doc, PalavraChave_CursoExtensao, '|X|X|X|')

        enum.add_item(bold('ÁREA TEMÁTICA PRINCIPAL: '))
        doc.append(NewLine())
        if curso.area_tematica_principal:
            tabela_alternativas(doc, AreaTematica, '|X|X|X|', id=curso.area_tematica_principal.id)

        enum.add_item(bold('ÁREA TEMÁTICA SECUNDÁRIA: '))
        doc.append(NewLine())
        if curso.area_tematica_secundaria:
            tabela_alternativas(doc, AreaTematica, '|X|X|X|', id=curso.area_tematica_secundaria.id)
        else:
            tabela_alternativas(doc, AreaTematica, '|X|X|X|')

        enum.add_item(bold('LINHA DE EXTENSÃO: '))
        doc.append(NewLine())
        doc.append(NoEscape(r'{\tiny'))
        if curso.linha_extensao:
            tabela_alternativas(doc, LinhaExtensao, 'X|X|X', id=curso.linha_extensao.id, hline=False)
        doc.append(NoEscape('}'))

        item(doc, enum, 'PÚBLICO ALVO: ', curso.publico_alvo)

        item(doc, enum, 'NÚMERO DE PESSOAS A SEREM BENEFICIADAS: ', curso.numero_pessoas_beneficiadas)

        item(doc, enum, 'CARGA HORÁRIA TOTAL: ', curso.carga_horaria_total)

        item(doc, enum, 'Nº DE VAGAS: ', curso.numero_vagas)

        item(doc, enum, 'LOCAL DA INSCRIÇÃO: ', curso.local_inscricao)

        # TODO: calibri 10, justificado (?), espaçamento simples (1,5?)
        enum.add_item(bold('RESUMO: '))
        doc.append(NewLine())
        doc.append(escape_latex(curso.resumo))

        item(doc, enum, 'PROGRAMAÇÃO: ', curso.programacao)

        enum.add_item(bold('EQUIPE DE TRABALHO: '))
        doc.append(NewLine())
        # TODO: se curso.servidores.all() for vazio, esse item fica vazio?
        for servidor in curso.servidores.all():
            servidor_cursoextensao = Servidor_CursoExtensao.objects.get(servidor_id=servidor.id)

            with doc.create(MdFramed(options=mdframed_options)):
                doc.append(bold('SERVIDORES UNIOESTE '))
                doc.append(NewLine())

                doc.append(NoEscape('Nome completo: '))
                doc.append(servidor.nome_completo)
                doc.append(NewLine())

                for obj in TipoServidor.objects.all():
                    if servidor.tipo.id == obj.id:
                        doc.append(NoEscape(r' ($\times$) ' + obj.nome + ' '))
                    else:
                        doc.append(' () ' + obj.nome + ' ')
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
                for obj in UnidadeAdministrativa.objects.all():
                    if servidor.unidade_administrativa and servidor.unidade_administrativa.id == obj.id:
                        doc.append(NoEscape(r'($\times$) ' + obj.nome + ' '))
                    else:
                        doc.append('() ' + obj.nome + ' ')

                if servidor.campus:
                    doc.append(NoEscape(r'($\times$) CAMPUS DE: '))
                    doc.append(servidor.campus)
                else:
                    doc.append(NoEscape(r'() CAMPUS DE: '))
                doc.append(NewLine())

                doc.append(NoEscape('E-mail: '))
                doc.append(escape_latex(servidor.email))
                doc.append(NewLine())

                # TODO: função pra isso: texto_livre(enunciado, dado=None, negrito=False)
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

        enum.add_item(bold('DISCENTES UNIOESTE: '))
        doc.append(NewLine())
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
        tab = tabela_discentes_membros(doc, cabecalho, table_spec)

        discentes = Discente_CursoExtensao.objects.filter(curso_extensao=curso.id)
        for discente in discentes:
            linha = [discente.nome,
                     discente.curso,
                     discente.serie,
                     discente.turno.nome,
                     discente.carga_horaria_semanal,
                     NoEscape(discente.telefone + ', \n' + '\leavevmode\hspace{0pt}' + escape_latex(discente.email))]
            tab.add_row(linha)
            tab.add_hline()

        doc.append(LineBreak())
        mdframed_options_plano = 'innertopmargin=5pt, innerleftmargin=3pt, innerrightmargin=3pt, topline=false'
        with doc.create(MdFramed(options=mdframed_options_plano)):
            doc.append(bold('PLANO DE TRABALHO: '))
            planos = []
            for discente in discentes:
                planos.append(discente.plano_trabalho)
            for plano in planos:
                doc.append(escape_latex(plano))
                doc.append(NewLine())

        doc.append(NoEscape('}')) # volta com tamanho da fonte normal

        enum.add_item(bold('MEMBROS DA COMUNIDADE / PARTICIPANTES EXTERNOS: '))
        doc.append(NewLine())
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
        tab = tabela_discentes_membros(doc, cabecalho, table_spec)

        membros = MembroComunidade_CursoExtensao.objects.filter(curso_extensao=curso.id)
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

        doc.append(LineBreak())
        mdframed_options_plano = 'innertopmargin=5pt, innerleftmargin=3pt, innerrightmargin=3pt, topline=false'
        with doc.create(MdFramed(options=mdframed_options_plano)):
            doc.append(bold('PLANO DE TRABALHO: '))
            planos = []
            for discente in discentes:
                planos.append(discente.plano_trabalho)
            for plano in planos:
                doc.append(escape_latex(plano))
                doc.append(NewLine())

        doc.append(NoEscape('}')) # volta com tamanho da fonte normal

        if PrevisaoOrcamentaria_CursoExtensao.objects.filter(curso_extensao=curso.id):
            formulario_previsao_orcamentaria(doc, enum, curso)

    doc.generate_pdf('curso_extensao/pdf/curso_extensao_' + str(curso.id))

# TODO: \\, \newline ou \linebreak?
# TODO: cabeçalho e numeração das páginas
# TODO: escape_latex e/ou NoEscape em tudo?
# TODO: checar se os objetos são nulos antes de colocar no PDF
