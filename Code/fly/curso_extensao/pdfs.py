# -*- coding: utf-8 -*-

import os
from pylatex import Enumerate, NoEscape, Command
from pylatex.utils import escape_latex

from base import pdfutils
from curso_extensao.models import PalavraChave_CursoExtensao, PrevisaoOrcamentaria_CursoExtensao
from fly.settings import PDF_DIR


def gerar_pdf_curso(curso):
    doc = pdfutils.init_document()

    pdfutils.pacotes(doc)

    # Configurações (preâmbulo)
    pdfutils.configuracoes_preambulo(doc)

    pdfutils.cabecalho(doc)

    frase_anexo = 'ANEXO V DA RESOLUÇÃO Nº 236/2014-CEPE, DE 13 DE NOVEMBRO DE 2014.'
    pdfutils.rodape(doc, NoEscape(r'\texttt{' + frase_anexo + '}'))
    doc.append(NoEscape(r'{\normalsize\texttt{' + frase_anexo + '}}'))

    pdfutils.titulo(doc, 'FORMULÁRIO ESPECÍFICO PARA ATIVIDADES DE EXTENSÃO', 'MODALIDADE CURSO DE EXTENSÃO')

    doc.append(Command('hrulefill'))

    # Início do formulário
    with doc.create(Enumerate()) as enum:
        pdfutils.item(doc, enum, 'TÍTULO: ', escape_latex(curso.titulo))

        pdfutils.item(doc, enum, 'COORDENADOR(a): ', escape_latex(curso.coordenador.nome_completo))

        periodo_inicio = curso.periodo_realizacao_inicio.strftime('%d/%m/%Y')
        periodo_fim = curso.periodo_realizacao_fim.strftime('%d/%m/%Y')
        periodo_realizacao = 'de {} a {}'.format(periodo_inicio, periodo_fim)
        pdfutils.item(doc, enum, 'PERÍODO DE REALIZAÇÃO: ', periodo_realizacao)

        pdfutils.mdframed_informar(doc, enum, curso.programa_extensao)

        pdfutils.tabela_unidade_administrativa(doc, enum, curso.unidade_administrativa, curso.campus)

        pdfutils.tabela_centro(doc, enum, curso.centro)

        pdfutils.tabela_grande_area(doc, enum, id=curso.grande_area.id)

        pdfutils.tabela_palavras_chave(doc, enum, PalavraChave_CursoExtensao.objects.filter(curso_extensao_id=curso.id))

        pdfutils.tabela_area_tematica_principal(doc, enum, id=curso.area_tematica_principal.id)

        if curso.area_tematica_secundaria:
            pdfutils.tabela_area_tematica_secundaria(doc, enum, id=curso.area_tematica_secundaria.id)
        else:
            pdfutils.tabela_area_tematica_secundaria(doc, enum)

        pdfutils.tabela_linha_extensao(doc, enum, curso.linha_extensao, id=curso.linha_extensao.id)

        pdfutils.item(doc, enum, 'PÚBLICO ALVO: ', escape_latex(curso.publico_alvo))

        pdfutils.item(doc, enum, 'NÚMERO DE PESSOAS A SEREM BENEFICIADAS: ', curso.numero_pessoas_beneficiadas)

        pdfutils.item(doc, enum, 'CARGA HORÁRIA TOTAL: ', curso.carga_horaria_total)

        pdfutils.item(doc, enum, 'Nº DE VAGAS: ', curso.numero_vagas)

        pdfutils.item(doc, enum, 'LOCAL DA INSCRIÇÃO: ', escape_latex(curso.local_inscricao))

        pdfutils.item(doc, enum, NoEscape(r'RESUMO: \\'))
        resumo_fmt = curso.resumo.replace('\r', '')
        doc.append(escape_latex(resumo_fmt))

        pdfutils.item(doc, enum, NoEscape(r'PROGRAMAÇÃO: \\'))
        programacao_fmt = curso.programacao.replace('\r', '')
        doc.append(escape_latex(programacao_fmt))

        pdfutils.item(doc, enum, NoEscape(r'EQUIPE DE TRABALHO: \\'))
        pdfutils.mdframed_equipe_trabalho(doc, curso)

        pdfutils.item(doc, enum, NoEscape(r'DISCENTES UNIOESTE: \\'))
        pdfutils.tabela_discentes(doc, curso)

        pdfutils.item(doc, enum, NoEscape(r'MEMBROS DA COMUNIDADE / PARTICIPANTES EXTERNOS: \\'))
        pdfutils.tabela_membros(doc, curso)

        # Checa antes pois a previsão orçamentária não é obrigatório
        if PrevisaoOrcamentaria_CursoExtensao.objects.filter(curso_extensao_id=curso.id):
            previsao_orcamentaria = PrevisaoOrcamentaria_CursoExtensao.objects.get(curso_extensao=curso.id)

            pdfutils.tabela_previsao_orcamentaria(doc, enum, previsao_orcamentaria)

            pdfutils.tabela_gestao_recursos_financeiros(doc, enum, previsao_orcamentaria)

    os.system('mkdir -p ' + PDF_DIR)

    filepath = '{}/curso-extensao_{}'.format(PDF_DIR, str(curso.id))
    doc.generate_pdf(filepath, clean_tex=False, compiler=pdfutils.COMPILER, compiler_args=pdfutils.COMPILER_ARGS)

    return filepath
