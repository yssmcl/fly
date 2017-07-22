# -*- coding: utf-8 -*-

from django.contrib.staticfiles.templatetags.staticfiles import static
import os
from pylatex import Enumerate, NoEscape, NewLine
from pylatex.utils import escape_latex

from base import pdfutils
from base.models import *
from curso_extensao.models import *
from fly.settings import PDF_DIR

def gerar_pdf(curso):
    doc = pdfutils.init_document()

    pdfutils.pacotes(doc)

    # Configurações (preâmbulo)
    pdfutils.configuracoes_preambulo(doc)

    pdfutils.cabecalho(doc)

    texto_anexo = NoEscape(r'\texttt{ANEXO V DA RESOLUÇÃO Nº 236/2014-CEPE, DE 13 DE NOVEMBRO DE 2014}')
    pdfutils.rodape(doc, texto_anexo)
    doc.append(texto_anexo)

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

        pdfutils.mdframed_informar(doc, enum, curso.programa_extensao)

        pdfutils.tabela_unidade_administrativa(doc, enum, curso.unidade_administrativa, curso.campus)

        pdfutils.tabela_centro(doc, enum, curso.centro)

        pdfutils.tabela_grande_area(doc, enum, id=curso.grande_area.id)

        pdfutils.tabela_palavras_chave(doc, enum, PalavraChave_CursoExtensao)

        pdfutils.tabela_area_tematica_principal(doc, enum, id=curso.area_tematica_principal.id)

        if curso.area_tematica_secundaria:
            pdfutils.tabela_area_tematica_secundaria(doc, enum, curso.area_tematica_secundaria, id=curso.area_tematica_secundaria.id)
        else:
            pdfutils.tabela_area_tematica_secundaria(doc, enum, curso.area_tematica_secundaria)

        pdfutils.tabela_linha_extensao(doc, enum, curso.linha_extensao, id=curso.linha_extensao.id)

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
        if PrevisaoOrcamentaria_CursoExtensao.objects.filter(curso_extensao=curso.id):
            previsao_orcamentaria = PrevisaoOrcamentaria_CursoExtensao.objects.get(curso_extensao=curso.id)

            pdfutils.tabela_previsao_orcamentaria(doc, enum, previsao_orcamentaria)

            pdfutils.tabela_gestao_recursos_financeiros(doc, enum, previsao_orcamentaria)

    os.system('mkdir -p ' + PDF_DIR)
    doc.generate_pdf(PDF_DIR + 'curso_extensao_' + str(curso.id), clean_tex=False)
