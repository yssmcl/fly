# -*- coding: utf-8 -*-

import os
from pylatex import Enumerate, NoEscape, NewLine, Center
from pylatex.utils import escape_latex, bold

from base import pdfutils
from base.models import EstadoProjeto
from fly.settings import PDF_DIR

def gerar_pdf_parecer(parecer):
    doc = pdfutils.init_document()

    pdfutils.pacotes(doc)

    # Configurações (preâmbulo)
    pdfutils.configuracoes_preambulo(doc)

    pdfutils.cabecalho(doc)

    frase_anexo = 'ANEXO XI DA RESOLUÇÃO Nº 236/2014-CEPE, DE 13 DE NOVEMBRO DE 2014.'
    pdfutils.rodape(doc, NoEscape(r'\texttt{' + frase_anexo + '}%'))
    doc.append(NoEscape(r'{\normalsize\texttt{' + frase_anexo + '}}%'))

    pdfutils.titulo(doc, 'RELATÓRIOS ESPECÍFICOS PARA ATIVIDADES DE EXTENSÃO', 'FORMULÁRIO ÚNICO DE PARECER DE ATIVIDADES DE EXTENSÃO')

    # Início do formulário
    with doc.create(Enumerate()) as enum:
        pdfutils.item(doc, enum, 'PARECER CONCLUSIVO DA COMISSÃO DE EXTENSÃO DE CENTRO')

    doc.append(bold('IDENTIFICAÇÃO:'))
    doc.append(NewLine())
    doc.append(NoEscape(r'Coordenador(a): {} \\'.format(escape_latex(parecer.projeto_extensao.coordenador.nome_completo))))
    doc.append(NoEscape(r'Colegiado: {} \\'.format(escape_latex(parecer.projeto_extensao.coordenador.colegiado))))
    doc.append(NoEscape(r'Centro: {} \\'.format(parecer.projeto_extensao.centro.nome)))
    doc.append(NoEscape(r'Campus: {} \\'.format(parecer.projeto_extensao.campus.nome)))
    doc.append(NoEscape(r'Título da atividade: {} \\ \\'.format(escape_latex(parecer.projeto_extensao.titulo))))
    # TODO: referente a portaria?
    # doc.append(NoEscape(r'Parecer referente a: \\ \\'))

    doc.append(bold('COMENTÁRIOS:'))
    doc.append(NewLine())
    pdfutils.tabela_alternativas(doc, EstadoProjeto, '|c|X|X|c|c|', id=parecer.estado_parecer.id)
    doc.append(NewLine())
    doc.append(NewLine())
    doc.append(NoEscape(r'Ata nº: {} \\'.format(escape_latex(parecer.numero_ata))))
    data = parecer.data.strftime('%d/%m/%Y')
    doc.append(NoEscape(r'Data: {} \\'.format(data)))

    texto = 'Carimbo e Assinatura do Coordenador(a) da Comissão de Extensão ou Representante Legal'
    largura = r'\widthof{{{}}}'.format(texto)
    pdfutils.assinatura(doc, texto, largura, Center())

    os.system('mkdir -p ' + PDF_DIR)

    filepath = '{}/parecer_{}_projeto_{}'.format(PDF_DIR, str(parecer.id), str(parecer.projeto_extensao.id))
    doc.generate_pdf(filepath, clean_tex=False, compiler=pdfutils.COMPILER, compiler_args=pdfutils.COMPILER_ARGS)

    return filepath
