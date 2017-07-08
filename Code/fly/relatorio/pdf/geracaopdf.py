from relatorio.models import *

def gerar_pdf(relatorio):
    from pylatex import Document, Enumerate, NoEscape, Package, Tabularx, FlushRight, \
         LineBreak, NewLine, MultiColumn, MultiRow, HFill, Table, Center
    from pylatex.base_classes import Environment
    from pylatex.utils import escape_latex, bold

    from relatorio.models import Relatorio, CertificadoRelatorio
    from base.models import UnidadeAdministrativa, Campus, Centro
    from curso_extensao.models import CursoExtensao

    width_argument = NoEscape(r'\linewidth')

    def tabela_participantes(doc, cabecalho, table_spec):
        from pylatex import Tabularx, NoEscape

        with doc.create(Tabularx('|' + table_spec, width_argument=width_argument)) as tab:
            tab.add_hline()
            tab.add_row(cabecalho)
            tab.add_hline()

            return tab

    def item(doc, enum, texto, dado=None):
        enum.add_item(bold(texto))
        if dado:
            doc.append(escape_latex(dado))


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
    #  doc.packages.add(Package('hyphenat', options='none')) # impede hifenização

    # Configuração da fonte sem serifa
    doc.append(NoEscape(r'\fontfamily{\sfdefault}\selectfont'))

    # Configuração das listas
    doc.preamble.append(NoEscape(r'''
    \setlist[enumerate, 1]{label*=\textbf{\arabic*}, leftmargin=*}
    \setlist[enumerate, 2]{label*=\textbf{.\arabic*}, leftmargin=*}
    '''))

    # Início do documento
    flush_right = FlushRight()
    flush_right.append(NoEscape(r'RELATÓRIOS ESPECÍFICOS PARA ATIVIDADES DE EXTENSÃO \\'))
    flush_right.append(NoEscape('RELATÓRIO DE EVENTOS E CURSOS'))
    doc.append(flush_right)

    doc.append(NoEscape('\hrulefill'))

    with doc.create(Enumerate()) as enum:
        doc.append(NoEscape(r'\footnotesize'))

        item(doc, enum, 'TÍTULO DA ATIVIDADE: ', relatorio.projeto_extensao.titulo)
        with doc.create(Enumerate()) as subenum:
            subenum.add_item(NoEscape('Vinculada a algum Programa de Extensão? '))
            if relatorio.projeto_extensao.programa_extensao:
                doc.append(NoEscape(r'Não () Sim ({$\times$}): Qual? '))
                doc.append(relatorio.projeto_extensao.programa_extensao.nome)
            else:
                doc.append(NoEscape(r'Não ($\times$) Sim (): Qual? '))

        item(doc, enum, 'COORDENADOR(a): ')

        periodo_inicio = relatorio.periodo_inicio.strftime('%d/%m/%Y')
        periodo_fim = relatorio.periodo_fim.strftime('%d/%m/%Y')
        periodo_realizacao = 'de {} a {}'.format(periodo_inicio, periodo_fim)
        item(doc, enum, 'PERÍODO DO RELATÓRIO: ', periodo_realizacao)

        item(doc, enum, 'UNIDADE ADMINISTRATIVA: ')
        for obj in UnidadeAdministrativa.objects.all():
            if relatorio.projeto_extensao.unidade_administrativa and relatorio.projeto_extensao.unidade_administrativa.id == obj.id:
                doc.append(NoEscape(obj.nome + r' ($\times$) '))
            else:
                doc.append(obj.nome + ' () ')
        doc.append(NewLine())

        doc.append(bold('CAMPUS DE: '))
        for obj in Campus.objects.all():
            if relatorio.projeto_extensao.campus and relatorio.projeto_extensao.campus.id == obj.id:
                doc.append(NoEscape(obj.nome + r' ($\times$) '))
            else:
                doc.append(obj.nome + ' () ')

        item(doc, enum, 'CENTRO: ')
        doc.append(NewLine())
        for obj in Centro.objects.all():
            if relatorio.projeto_extensao.centro and relatorio.projeto_extensao.centro.id == obj.id:
                doc.append(NoEscape(obj.nome + r' ($\times$) '))
            else:
                doc.append(obj.nome + ' () ')

        curso = CursoExtensao.objects.get(id=relatorio.projeto_extensao.id)
        #  colegiado = curso.colegiado.nome
        #  item(doc, enum, 'COLEGIADO: ', colegiado)
        item(doc, enum, 'COLEGIADO: ')

        item(doc, enum, 'PÚBLICO ATINGIDO: ', relatorio.publico_atingido)

        item(doc, enum, 'CERTIFICADOS: ', relatorio.publico_atingido)
        with doc.create(Enumerate()) as subenum:
            subenum.add_item('Relacionar o nome dos participantes com direito a certificados.')
            doc.append(NewLine())
            #  doc.append(NewLine())
            table_spec = NoEscape(r'''>{\centering\arraybackslash}X|
                                  @{    }c@{    }|
                                  @{    }c@{    }|
                                  @{    }c@{    }|
                                  ''')
            cabecalho = ['NOME',
                         'FUNÇÃO',
                         'FREQUÊNCIA (%)',
                         'C/H TOTAL']

            tab = tabela_participantes(doc, cabecalho, table_spec)

            # TODO: teste
            #  certificado = CertificadoRelatorio.objects.filter(relatorio=relatorio_id)
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
            subenum.add_item('Informar se os certificados devem ser emitidos: ')
            doc.append(NoEscape('() pela PROEX \hfill () pelo Centro da Coordenação ou Órgão Promotor'))

        item(doc, enum, 'RESUMO DA ATIVIDADE REALIZADA: ', relatorio.resumo)

        item(doc, enum, 'RELACIONAR AS ATIVIDADES REALIZADAS OU A PROGRAMAÇÃO PARA CURSOS OU EVENTOS: ', relatorio.atividades_realizadas_programacao)

        item(doc, enum, 'RELACIONAR AS DIFICULDADES TÉCNICAS E/OU ADMINISTRATIVAS (se houver): ', relatorio.dificuldades)

    center = Center()
    center.append(NoEscape('\hrulefill'))
    center.append(NewLine())
    center.append(NoEscape(r'Local e data \\'))
    center.append(NoEscape('\hrulefill'))
    center.append(NewLine())
    center.append(NoEscape('Assinatura do(a) Coordenador(a) da Atividade'))
    doc.append(center)

    doc.generate_pdf('relatorio/pdf/relatorio_' + str(relatorio.id))

# TODO: teste
gerar_pdf(Relatorio.objects.all().first())

# TODO: checar se os objetos são nulos antes de colocar no PDF
