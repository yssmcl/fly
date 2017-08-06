# -*- coding: utf-8 -*-

import os
from pylatex import Document, Enumerate, NoEscape, Package, Tabularx, FlushRight, \
     LineBreak, NewLine, MultiColumn, MultiRow, HFill, Table, Center
from pylatex.base_classes import Environment
from pylatex.utils import escape_latex, bold

from base import pdfutils
from base.models import UnidadeAdministrativa, Campus, Centro, EstadoProjeto
from curso_extensao.models import CursoExtensao
from fly.settings import PDF_DIR

def gerar_pdf(parecer):
    doc = pdfutils.init_document()

    pdfutils.pacotes(doc)

    # Configurações (preâmbulo)
    pdfutils.configuracoes_preambulo(doc)

    pdfutils.cabecalho(doc)

    texto_anexo = NoEscape(r'\texttt{ANEXO XI DA RESOLUÇÃO Nº 236/2014-CEPE, DE 13 DE NOVEMBRO DE 2014.}')
    pdfutils.rodape(doc, texto_anexo)
    doc.append(texto_anexo)

    pdfutils.titulo(doc, 'RELATÓRIOS ESPECÍFICOS PARA ATIVIDADES DE EXTENSÃO',
                    'FORMULÁRIO ÚNICO DE PARECER DE ATIVIDADES DE EXTENSÃO')

    # Início do formulário
    with doc.create(Enumerate()) as enum:
        doc.append(NoEscape(r'\footnotesize'))

        pdfutils.item(doc, enum, 'PARECER CONCLUSIVO DA COMISSÃO DE EXTENSÃO DE CENTRO')

    doc.append(bold('IDENTIFICAÇÃO:'))
    doc.append(NewLine())
    doc.append(NoEscape(r'Coordenador(a): {} \\'.format(escape_latex(parecer.projeto_extensao.coordenador.nome_completo))))
    doc.append(NoEscape(r'Colegiado: {} \\'.format(escape_latex(parecer.projeto_extensao.coordenador.colegiado))))
    doc.append(NoEscape(r'Centro: {} \\'.format(escape_latex(parecer.projeto_extensao.centro.nome))))
    doc.append(NoEscape(r'Campus: {} \\'.format(escape_latex(parecer.projeto_extensao.campus.nome))))
    doc.append(NoEscape(r'Título da atividades: {} \\'.format(escape_latex(parecer.projeto_extensao.titulo))))
    doc.append(NoEscape(r'Parecer referente a: \\ \\')) # TODO: referente a portaria?

    doc.append(bold('COMENTÁRIOS:'))
    doc.append(NewLine())
    # for estado in UnidadeAdministrativa.objects.all():
    #     if parecer.estado_parecer and parecer.estado_parecer.id == estado.id:
    #         doc.append(NoEscape(r'{} ({}) '.format(estado.nome, times)))
    #     else:
    #         doc.append(NoEscape(r'{} ({}) '.format(estado.nome, phantom)))
    # table_spec = NoEscape(r'''|>{\centering\arraybackslash}c|
    #                           >{\centering\arraybackslash}X|
    #                           >{\centering\arraybackslash}X|
    #                           >{\centering\arraybackslash}c|
    #                           >{\centering\arraybackslash}c|
    #                       ''')
    pdfutils.tabela_alternativas(doc, EstadoProjeto, '|c|X|X|c|c|', id=parecer.estado_parecer.id)

    doc.append(NewLine())

    # doc.append(NoEscape('Ata nº: {} \\'.format(parecer.numero_ata)))
    # data = parecer.data.strftime('%d/%m/%Y'),
    # doc.append(NoEscape('Data: {} \\'.format(data)))
    # pdfutils.assinatura(doc, 'Carimbo e Assinatura do Coordenador(a) da Comissão de Extensão ou Representante Legal',
    #                     '.8\textwidth')

    os.system('mkdir -p ' + PDF_DIR)

    # TODO: UnicodeDecodeError
    # try:
    filepath = '{}/parecer_{}_projeto_{}'.format(PDF_DIR, str(parecer.id), str(parecer.projeto_extensao.id))
    doc.generate_pdf(filepath, clean_tex=False)
    # except UnicodeDecodeError:
        # pass

    return filepath
