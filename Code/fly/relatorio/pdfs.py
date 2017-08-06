# -*- coding: utf-8 -*-

import os
from pylatex import Enumerate, NoEscape, NewLine
from pylatex.utils import escape_latex

from base import pdfutils
from fly.settings import PDF_DIR

def gerar_pdf_relatorio(relatorio):
    doc = pdfutils.init_document()

    pdfutils.pacotes(doc)

    # Configurações (preâmbulo)
    pdfutils.configuracoes_preambulo(doc)

    pdfutils.cabecalho(doc)

    texto_anexo = NoEscape(r'\texttt{ANEXO X DA RESOLUÇÃO Nº 236/2014-CEPE, DE 13 DE NOVEMBRO DE 2014.}')
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
                doc.append(NoEscape(r'Não ({}) Sim ({}): Qual? {}'.format(pdfutils.PHANTOM, pdfutils.TIMES,
                    relatorio.projeto_extensao.programa_extensao.nome)))
            else:
                doc.append(NoEscape(r'Não ({}) Sim ({}): Qual? '.format(pdfutils.TIMES, pdfutils.PHANTOM)))

        pdfutils.item(doc, enum, 'COORDENADOR(a): ', relatorio.projeto_extensao.coordenador.nome_completo)

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
        resumo_fmt = escape_latex(relatorio.resumo.replace('\r', ''))
        doc.append(escape_latex(resumo_fmt))

        pdfutils.item(doc, enum, 'RELACIONAR AS ATIVIDADES REALIZADAS OU A PROGRAMAÇÃO PARA CURSOS OU EVENTOS: ')
        doc.append(NewLine())
        atividades_fmt = escape_latex(relatorio.atividades_realizadas_programacao.replace('\r', ''))
        doc.append(atividades_fmt)

        pdfutils.item(doc, enum, 'RELACIONAR AS DIFICULDADES TÉCNICAS E/OU ADMINISTRATIVAS (se houver): ')
        doc.append(NewLine())
        dificuldades_fmt = escape_latex(relatorio.dificuldades.replace('\r', ''))
        doc.append(dificuldades_fmt)

    pdfutils.local_data_assinatura(doc)

    os.system('mkdir -p ' + PDF_DIR)

    filepath = '{}/relatorio_{}'.format(PDF_DIR, str(relatorio.id))
    doc.generate_pdf(filepath, clean_tex=False, compiler=pdfutils.COMPILER, compiler_args=pdfutils.COMPILER_ARGS)

    return filepath
