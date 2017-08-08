import os
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.encoding import smart_str
from django.views import View, generic
from django.urls import reverse
from django.core.exceptions import PermissionDenied

from .forms import ParecerForm
from .models import Parecer
from curso_extensao.models import CursoExtensao
from parecer.pdfs import *
from base.utils import send_email_docente

class NovoParecer(LoginRequiredMixin, View):
    def get(self, request, pk):
        form = ParecerForm()

        projeto_extensao = get_object_or_404(CursoExtensao, pk=pk)

        return render(request, 'parecer/parecer_form.html',
                      {'form': form, 'projeto_extensao': projeto_extensao})

    def post(self, request, pk):
        form = ParecerForm(request.POST)

        parecer = form.instance

        parecer.projeto_extensao = get_object_or_404(CursoExtensao, pk=pk)

        #TODO: verificar se .user pertence a comissao

        if parecer.projeto_extensao.estado.nome not in {'Submetido'}:
            raise PermissionDenied

        if form.is_valid():
            with transaction.atomic():
                form.save()
                parecer.projeto_extensao.estado = parecer.estado_parecer
                parecer.projeto_extensao.save()

            send_email_docente(parecer.projeto_extensao.coordenador, "[SGPE] Submissão de parecer", 'Seu Curso de Extensão recebeu um parecer, acesse-o neste <a href="http://cacc.unioeste-foz.br:8000' + reverse('parecer:consulta', args=[pk]) + '">link</a>.')

            return redirect('parecer:consulta', pk)
        else:
            return render(request, 'parecer/parecer_form.html',
                          {'form': form, 'projeto_extensao': parecer.projeto_extensao})


class ConsultaParecer(LoginRequiredMixin, View):
    def get(self, request, pk):
        projeto_extensao = get_object_or_404(CursoExtensao, pk=pk)
        object_list = Parecer.objects.filter(projeto_extensao=projeto_extensao)

        return render(request, 'parecer/parecer_list.html',
                      {'projeto_extensao':projeto_extensao, 'object_list':object_list})


class DetalheParecer(LoginRequiredMixin, View):
    def get(self, request, pk):
        parecer = get_object_or_404(Parecer, pk=pk)

        form = ParecerForm(instance=parecer)

        return render(request, 'parecer/parecer_form.html',
                      {'form': form, 'projeto_extensao': parecer.projeto_extensao})

    def post(self, request, pk):
        parecer = get_object_or_404(Parecer, pk=pk)

        form = ParecerForm(request.POST, instance=parecer)

        parecer = form.instance

        #TODO: verificar se .user pertence a comissao

        if form.is_valid():
            with transaction.atomic():
                form.save()
                parecer.projeto_extensao.estado = parecer.estado_parecer
                parecer.projeto_extensao.save()

            return redirect('parecer:consulta', parecer.projeto_extensao.pk)

        else:
            return render(request, 'parecer/parecer_form.html',
                          {'form': form, 'projeto_extensao': parecer.projeto_extensao})


class DeletarParecer(LoginRequiredMixin, View):
    def post(self, request):
        parecer = get_object_or_404(Parecer, pk=request.POST['pk'])

        #TODO: verificar se .user pertence a comissao

        parecer.delete()
        return redirect('parecer:consulta', parecer.projeto_extensao.pk)


class GeracaoPDFParecer(LoginRequiredMixin, View):
    def get(self, request, pk):
        parecer = get_object_or_404(Parecer, pk=pk)

        caminho = gerar_pdf_parecer(parecer) + '.pdf'

        with open(caminho, 'rb') as arquivo_pdf:
            response = HttpResponse(arquivo_pdf, content_type='application/pdf')
            # Abre no visualizador de PDFs do navegador
            nome_arquivo = caminho.split(os.sep)[-1]
            response['Content-Disposition'] = 'inline; filename={}'.format(smart_str(nome_arquivo))

            return response
