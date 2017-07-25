# -*- coding: utf-8 -*-

import os
from pylatex import Document, Enumerate, NoEscape, Package, Tabularx, FlushRight, \
     LineBreak, NewLine, MultiColumn, MultiRow, HFill, Table, Center
from pylatex.base_classes import Environment
from pylatex.utils import escape_latex, bold

from base import pdfutils
from base.models import UnidadeAdministrativa, Campus, Centro
from curso_extensao.models import CursoExtensao
from fly.settings import PDF_DIR
from relatorio.models import Relatorio, CertificadoRelatorio

def gerar_pdf(relatorio):
    times = NoEscape(r'$\times$')
    phantom = NoEscape(r'\phantom{$\times$}')

    doc = pdfutils.init_document()

    pdfutils.pacotes(doc)

    # Configurações (preâmbulo)
    pdfutils.configuracoes_preambulo(doc)

    pdfutils.cabecalho(doc)

    texto_anexo = NoEscape(r'\texttt{ANEXO X DA RESOLUÇÃO Nº 236/2014-CEPE, DE 13 DE NOVEMBRO DE 2014}')
    pdfutils.rodape(doc, texto_anexo)
    doc.append(texto_anexo)

    pdfutils.titulo(doc, 'RELATÓRIOS ESPECÍFICOS PARA ATIVIDADES DE EXTENSÃO', 'RELATÓRIO DE EVENTOS E CURSOS')

    doc.append(NoEscape('\hrulefill'))

    # Início do formulário
    with doc.create(Enumerate()) as enum:
        doc.append(NoEscape(r'\footnotesize'))

        pdfutils.item(doc, enum, 'TÍTULO DA ATIVIDADE: ', relatorio.projeto_extensao.titulo)
        with doc.create(Enumerate()) as subenum:
            subenum.add_item(NoEscape('Vinculada a algum Programa de Extensão? '))
            if relatorio.projeto_extensao.programa_extensao:
                doc.append(NoEscape(r'Não ({}) Sim ({}): Qual? {}'.format(phantom, times,
                    relatorio.projeto_extensao.programa_extensao.nome)))
            else:
                doc.append(NoEscape(r'Não ({}) Sim ({}): Qual? '.format(times, phantom)))

        pdfutils.item(doc, enum, 'COORDENADOR(a): ')

        periodo_inicio = relatorio.periodo_inicio.strftime('%d/%m/%Y')
        periodo_fim = relatorio.periodo_fim.strftime('%d/%m/%Y')
        periodo_realizacao = 'de {} a {}'.format(periodo_inicio, periodo_fim)
        pdfutils.item(doc, enum, 'PERÍODO DO RELATÓRIO: ', periodo_realizacao)

        pdfutils.tabela_unidade_administrativa(doc, enum, relatorio.projeto_extensao.unidade_administrativa,
                                               relatorio.projeto_extensao.campus)

        pdfutils.tabela_centro(doc, enum, relatorio.projeto_extensao.centro)

        pdfutils.item(doc, enum, 'COLEGIADO: ', relatorio.projeto_extensao.coordenador.colegiado)

        pdfutils.item(doc, enum, 'PÚBLICO ATINGIDO: ', relatorio.publico_atingido)

        pdfutils.item(doc, enum, 'CERTIFICADOS: ')
        pdfutils.tabela_certificados(doc, id=relatorio.id)

        pdfutils.item(doc, enum, 'RESUMO DA ATIVIDADE REALIZADA: ')
        doc.append(NewLine())
        doc.append(escape_latex(relatorio.resumo))

        pdfutils.item(doc, enum, 'RELACIONAR AS ATIVIDADES REALIZADAS OU A PROGRAMAÇÃO PARA CURSOS OU EVENTOS: ')
        doc.append(NewLine())
        doc.append(escape_latex(relatorio.atividades_realizadas_programacao))

        pdfutils.item(doc, enum, 'RELACIONAR AS DIFICULDADES TÉCNICAS E/OU ADMINISTRATIVAS (se houver): ')
        doc.append(NewLine())
        doc.append(escape_latex(relatorio.dificuldades))

    pdfutils.local_data_assinatura(doc)

    os.system('mkdir -p ' + PDF_DIR)


    try:
        doc.generate_pdf(PDF_DIR + 'relatorio_' + str(relatorio.id), clean_tex=False)
    except UnicodeDecodeError:
        pass
