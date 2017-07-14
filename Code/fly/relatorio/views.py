from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.encoding import smart_str
from django.views import View, generic

from .forms import RelatorioForm, CertificadoRelatorioFormSet, FileUploadFormSet
from .models import Relatorio
from curso_extensao.models import CursoExtensao
from relatorio.pdfs import gerar_pdf

class NovoRelatorio(View):
    def get(self, request, pk):
        main_form = RelatorioForm(prefix='main')
        certificados_formset = CertificadoRelatorioFormSet(prefix='certificados')

        projeto_extensao = get_object_or_404(CursoExtensao, pk=pk)

        certificados_formset.can_delete = False

        return render(request, 'relatorio/relatorio_form.html', {'main_form':main_form, 'certificados_formset':certificados_formset, 'projeto_extensao':projeto_extensao})

    def post(self, request, pk):
        main_form = RelatorioForm(request.POST, prefix='main')

        relatorio = main_form.instance

        certificados_formset = CertificadoRelatorioFormSet(request.POST, instance=relatorio, prefix='certificados')

        relatorio.projeto_extensao = get_object_or_404(CursoExtensao, pk=pk)

        if (main_form.is_valid()
                and certificados_formset.is_valid()):

            with transaction.atomic():
                main_form.save()
                certificados_formset.save()

            return redirect('curso_extensao:index')
        else:
            certificados_formset.can_delete = False

            return render(request, 'relatorio/relatorio_form.html', {'main_form': main_form, 'certificados_formset': certificados_formset, 'projeto_extensao': relatorio.projeto_extensao})


class ConsultaRelatorio(View):
    def get(self, request, pk):
        projeto_extensao = get_object_or_404(CursoExtensao, pk=pk)
        object_list = Relatorio.objects.filter(projeto_extensao=projeto_extensao)

        return render(request, 'relatorio/relatorio_list.html', {'projeto_extensao':projeto_extensao, 'object_list':object_list})


class DetalheRelatorio(View):
    def get(self, request, pk):
        relatorio = get_object_or_404(Relatorio, pk=pk)

        main_form = RelatorioForm(instance=relatorio, prefix='main')
        certificados_formset = CertificadoRelatorioFormSet(instance=relatorio, prefix='certificados')

        return render(request, 'relatorio/relatorio_form.html', {'main_form':main_form, 'certificados_formset':certificados_formset, 'projeto_extensao':relatorio.projeto_extensao})

    def post(self, request, pk):
        relatorio = get_object_or_404(Relatorio, pk=pk)

        main_form = RelatorioForm(request.POST, instance=relatorio, prefix='main')
        certificados_formset = CertificadoRelatorioFormSet(request.POST, instance=relatorio, prefix='certificados')

        if (main_form.is_valid()
                and certificados_formset.is_valid()):

            with transaction.atomic():
                main_form.save()
                certificados_formset.save()

            return redirect('curso_extensao:index')
        else:
            return render(request, 'relatorio/relatorio_form.html', {'main_form': main_form, 'certificados_formset': certificados_formset, 'projeto_extensao': relatorio.projeto_extensao})


class GeracaoPDFRelatorio(LoginRequiredMixin, View):
    def get(self, request, pk):
        relatorio = get_object_or_404(Relatorio, pk=pk)
        gerar_pdf(relatorio)
        caminho_arquivo = 'relatorio/pdf/'
        nome_arquivo = 'relatorio_{}.pdf'.format(str(pk))

        arquivo_pdf = open(caminho_arquivo + nome_arquivo, 'rb')
        response = HttpResponse(arquivo_pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename=%s' % smart_str(nome_arquivo)
        return response
