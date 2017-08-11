# -*- coding: utf-8 -*-

import os
import locale
from django.utils import timezone
from pylatex import Document, Package, Enumerate, NoEscape, NewLine, FlushRight, FlushLeft, \
     StandAloneGraphic, VerticalSpace, HorizontalSpace, LineBreak, LargeText, MiniPage, Center, Command, UnsafeCommand
from pylatex.utils import escape_latex

from base import pdfutils
from relatorio.models import CertificadoRelatorio
from fly.settings import PDF_DIR, BASE_DIR

def gerar_pdf_relatorio(relatorio):
    doc = pdfutils.init_document()

    pdfutils.pacotes(doc)

    # Configurações (preâmbulo)
    pdfutils.configuracoes_preambulo(doc)

    pdfutils.cabecalho(doc)

    frase_anexo = 'ANEXO X DA RESOLUÇÃO Nº 236/2014-CEPE, DE 13 DE NOVEMBRO DE 2014.'
    pdfutils.rodape(doc, NoEscape(r'\texttt{' + frase_anexo + '}%'))
    doc.append(NoEscape(r'{\normalsize\texttt{' + frase_anexo + '}}%'))

    pdfutils.titulo(doc, 'RELATÓRIOS ESPECÍFICOS PARA ATIVIDADES DE EXTENSÃO', 'RELATÓRIO DE EVENTOS E CURSOS')

    doc.append(Command('hrulefill%'))

    # Início do formulário
    with doc.create(Enumerate()) as enum:
        pdfutils.item(doc, enum, 'TÍTULO DA ATIVIDADE: ', escape_latex(relatorio.projeto_extensao.titulo))
        with doc.create(Enumerate()) as subenum:
            subenum.add_item('Vinculada a algum Programa de Extensão? ')
            if relatorio.projeto_extensao.programa_extensao:
                doc.append(NoEscape(r'Não ({}) Sim ({}): Qual? {}'.format(pdfutils.PHANTOM, pdfutils.TIMES,
                                                                           escape_latex(relatorio.projeto_extensao.programa_extensao.nome))))
            else:
                doc.append(NoEscape(r'Não ({}) Sim ({}): Qual? '.format(pdfutils.TIMES, pdfutils.PHANTOM)))

        pdfutils.item(doc, enum, 'COORDENADOR(a): ', escape_latex(relatorio.projeto_extensao.coordenador.nome_completo))

        periodo_inicio = relatorio.periodo_inicio.strftime('%d/%m/%Y')
        periodo_fim = relatorio.periodo_fim.strftime('%d/%m/%Y')
        periodo_realizacao = 'de {} a {}'.format(periodo_inicio, periodo_fim)
        pdfutils.item(doc, enum, 'PERÍODO DO RELATÓRIO: ', periodo_realizacao)

        pdfutils.tabela_unidade_administrativa(doc, enum, relatorio.projeto_extensao.unidade_administrativa,
                                               relatorio.projeto_extensao.campus)

        pdfutils.tabela_centro(doc, enum, relatorio.projeto_extensao.centro)

        pdfutils.item(doc, enum, 'COLEGIADO: ', escape_latex(relatorio.projeto_extensao.coordenador.colegiado))

        pdfutils.item(doc, enum, 'PÚBLICO ATINGIDO: ', escape_latex(relatorio.publico_atingido))

        pdfutils.item(doc, enum, 'CERTIFICADOS: ')
        pdfutils.tabela_certificados(doc, id=relatorio.id)

        pdfutils.item(doc, enum, NoEscape(r'RESUMO DA ATIVIDADE REALIZADA: \\'))
        resumo_fmt = escape_latex(relatorio.resumo.replace('\r', ''))
        doc.append(escape_latex(resumo_fmt))

        pdfutils.item(doc, enum, NoEscape(r'RELACIONAR AS ATIVIDADES REALIZADAS OU A PROGRAMAÇÃO PARA CURSOS OU EVENTOS: \\'))
        atividades_fmt = relatorio.atividades_realizadas_programacao.replace('\r', '')
        doc.append(escape_latex(atividades_fmt))

        pdfutils.item(doc, enum, NoEscape(r'RELACIONAR AS DIFICULDADES TÉCNICAS E/OU ADMINISTRATIVAS (se houver): \\'))
        dificuldades_fmt = relatorio.dificuldades.replace('\r', '')
        doc.append(escape_latex(dificuldades_fmt))

    pdfutils.local_data_assinatura(doc)

    os.system('mkdir -p ' + PDF_DIR)

    filepath = '{}/relatorio_{}'.format(PDF_DIR, str(relatorio.id))
    doc.generate_pdf(filepath, clean_tex=False, compiler=pdfutils.COMPILER, compiler_args=pdfutils.COMPILER_ARGS)

    return filepath


def gerar_pdf_certificado(certificado):

    # Configurações da classe
    geometry_options = {'landscape': True,
                        'left': '2cm',
                        'right': '1cm'}
    doc = Document(geometry_options=geometry_options, lmodern=False, document_options=['a4paper', 'brazil'],
                   inputenc=None, fontenc=None, font_size='footnotesize')

    # Pacotes
    doc.packages.add(Package('microtype'))
    doc.packages.add(Package('indentfirst'))
    doc.packages.add(Package('graphicx'))
    doc.packages.add(Package('calc'))
    doc.packages.add(Package('fontspec'))
    options_background = ['scale=1',
                          'opacity=1',
                          'angle=0']
    doc.packages.add(Package('background', options=options_background))
    doc.packages.add(Package('csquotes'))

    # Configurações (preâmbulo)
    doc.preamble.append(Command('MakeOuterQuote', '\"')) # coverte aspas automaticamente, sem precisar de `` e ''
    doc.preamble.append(Command('renewcommand', arguments=[Command('baselinestretch'), '1.5']))
    doc.preamble.append(Command('setlength', arguments=[Command('parindent'), NoEscape(r'.35\textwidth')]))
    doc.preamble.append(Command('setlength', arguments=[Command('parskip'), '0.2cm']))
    doc.preamble.append(Command('setlength', arguments=[Command('emergencystretch'), '5pt']))

    # Imagem de fundo
    doc.preamble.append(NoEscape(r'\backgroundsetup{ contents=\includegraphics{modelo-certificado-20.pdf} }'))

    # Diretório das imagens
    img_dir = '{}/base/static/img/'.format(BASE_DIR) # necessário barra no final
    doc.preamble.append(UnsafeCommand('graphicspath', '{{{}}}'.format(img_dir)))

    # Início do documento
    doc.append(UnsafeCommand('setmainfont', 'Latin Modern Sans', 'SizeFeatures={Size=16}'))

    doc.append(Command('pagestyle', 'empty'))
    doc.append(Command('BgThispage'))

    doc.append(VerticalSpace(size='2cm', star=True))

    with doc.create(FlushRight()) as fr:
        fr.append(StandAloneGraphic('titulo-certificado.pdf', 'width=6.5cm'))
        fr.append(LineBreak())

    doc.append(VerticalSpace(size=NoEscape('-1cm'), star=True))
    doc.append(Command('Large'))

    # Usado para o nome dos meses ('%B')
    locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

    inicio = certificado.relatorio.periodo_inicio.strftime('%d de %B de %Y').lower()
    fim = certificado.relatorio.periodo_inicio.strftime('%d de %B de %Y').lower()
    # TODO: tá faltando coisa
    texto_principal = r'''

    Certificamos que \textbf{{{nome}}} atuou como {funcao}, {sob_coordenacao}no período de {inicio} a {fim}, na cidade de Foz do Iguaçu -- Paraná, com a atividade de extensão: "\textbf{{{titulo}}}", com carga horária de {carga_horaria_total} horas.

    '''

    if certificado.funcao.nome == 'Coordenador(a)':
        sob_coordenacao = ''
    else:
        nome_coordenador = certificado.relatorio.projeto_extensao.coordenador.nome_completo
        sob_coordenacao = r'sob a coordenação de \textbf{{{}}}, '.format(escape_latex(nome_coordenador))

    texto_principal = texto_principal.format(nome=escape_latex(certificado.nome),
                                             funcao=certificado.funcao.nome.lower(),
                                             sob_coordenacao=sob_coordenacao,
                                             inicio=inicio,
                                             fim=fim,
                                             titulo=escape_latex(certificado.relatorio.projeto_extensao.titulo),
                                             carga_horaria_total=str(certificado.carga_horaria_total).split('.')[0])

    # texto_principal = NoEscape(r'''

    # Certificamos que \textbf{Adriana de Oliveira Gomes} participou como bolsista do Programa de Apoio a Inclusão Social em Atividades de Extensão -- Convênio No 750/2014 -- Fundação Araucária, Edital 05/2014-PROEX, sob a orientação do (a) professor (a) \textbf{Fernando Amâncio Aragão}, no período de outubro/2014 a setembro/2015, com a atividade de extensão: \textbf{''Atendimento fisioterapêutico para pacientes com sequelas neurológicas baseada em tarefas funcionais.''}, com carga horária de 960 (novecentas e sessenta) horas.

    # ''')

    doc.append(NoEscape(texto_principal))

    doc.append(VerticalSpace(size='1.5cm', star=True))

    doc.append(HorizontalSpace(size='7cm', star=True))
    dia = timezone.now().strftime('%d')
    mes = timezone.now().strftime('%B')
    ano = timezone.now().strftime('%Y')

    data = NoEscape(r'Foz do Iguaçu, {} de {} de {}'.format(dia, mes, ano))
    largura = Command('widthof', data).dumps()
    with doc.create(MiniPage(width=largura)) as mini:
        with mini.create(Center()) as center:
            center.append(data)
            center.append(NewLine())
            center.append(NewLine())
            center.append(NewLine())
            center.append('Coordenador do Projeto de Extensão')
            center.append(NewLine())
            center.append(NewLine())
            center.append(NewLine())
            center.append('Diretor de Centro')

    os.system('mkdir -p ' + PDF_DIR)

    filepath = '{}/certificado_{}'.format(PDF_DIR, str(certificado.id))
    doc.generate_pdf(filepath, clean_tex=False, compiler=pdfutils.COMPILER, compiler_args=pdfutils.COMPILER_ARGS)

    return filepath
