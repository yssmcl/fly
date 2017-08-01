from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.encoding import smart_str
from django.views import View, generic

from .forms import RelatorioForm, RelatorioFileForm, CertificadoRelatorioFormSet
from .models import Relatorio, RelatorioFile, EstadoRelatorio
from curso_extensao.models import CursoExtensao
from relatorio.pdfs import gerar_pdf
from fly.settings import PDF_DIR, MEDIA_ROOT

import subprocess

class NovoRelatorio(LoginRequiredMixin, View):
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

            # Set extra data
            relatorio.estado = EstadoRelatorio.objects.get(nome='Não submetido')

            with transaction.atomic():
                main_form.save()
                certificados_formset.save()

            return redirect('relatorio:consulta', pk)
        else:
            certificados_formset.can_delete = False

            return render(request, 'relatorio/relatorio_form.html', {'main_form': main_form, 'certificados_formset': certificados_formset, 'projeto_extensao': relatorio.projeto_extensao})


class ConsultaRelatorio(LoginRequiredMixin, View):
    def get(self, request, pk):
        projeto_extensao = get_object_or_404(CursoExtensao, pk=pk)
        object_list = Relatorio.objects.filter(projeto_extensao=projeto_extensao)

        return render(request, 'relatorio/relatorio_list.html', {'projeto_extensao':projeto_extensao, 'object_list':object_list})


class DetalheRelatorio(LoginRequiredMixin, View):
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

            return redirect('relatorio:consulta', relatorio.projeto_extensao.pk)
        else:
            return render(request, 'relatorio/relatorio_form.html', {'main_form': main_form, 'certificados_formset': certificados_formset, 'projeto_extensao': relatorio.projeto_extensao})


class UploadArquivoRelatorio(LoginRequiredMixin, View):
    def get(self, request, pk):
        relatorio = get_object_or_404(Relatorio, pk=pk)

        file_form = RelatorioFileForm()

        return render(request, 'relatorio/upload_form.html', {'file_form':file_form})

    def post(self, request, pk):
        relatorio = get_object_or_404(Relatorio, pk=pk)

        file_form = RelatorioFileForm(request.POST, request.FILES)
        file_instance = file_form.instance
        file_instance.relatorio = relatorio

        if file_form.is_valid():
            file_instance.nome = file_instance.file.name
            file_form.save()

            return redirect('relatorio:lista_arquivos', relatorio.pk)
        else:
            return render(request, 'relatorio/upload_form.html', {'file_form':file_form})


class ListaArquivosRelatorio(LoginRequiredMixin, View):
    def get(self, request, pk):
        relatorio = get_object_or_404(Relatorio, pk=pk)
        object_list = relatorio.relatoriofile_set.all()

        return render(request, 'relatorio/relatoriofile_list.html', {'relatorio':relatorio, 'object_list':object_list})


class DownloadArquivoRelatorio(LoginRequiredMixin, View):
    def get(self, request, pk):
        relatorio_file = get_object_or_404(RelatorioFile, pk=pk)
        file = relatorio_file.file

        response = HttpResponse(file, content_type='application/force-download')
        response['Content-Disposition'] = 'attachment; filename=%s' % smart_str(relatorio_file.nome)
        response['Content-Length'] = file.size
        # response['X-Sendfile'] = smart_str(MEDIA_ROOT+file.name)

        return response


class DeletarArquivoRelatorio(LoginRequiredMixin, View):
    def post(self, request):
        file = get_object_or_404(RelatorioFile, pk=request.POST['pk'])
        relatorio = file.relatorio
        if file.relatorio.projeto_extensao.user == request.user:
            file.delete()
            return redirect('relatorio:lista_arquivos', relatorio.pk)
        else:
            return redirect('base:index') #TODO: mensagem de erro


class GeracaoPDFRelatorio(LoginRequiredMixin, View):
    def get(self, request, pk):
        relatorio = get_object_or_404(Relatorio, pk=pk)

        try:
            gerar_pdf(relatorio)
        except subprocess.CalledProcessError:
            pass
            
        nome_arquivo = 'relatorio_{}.pdf'.format(str(pk))

        with open(PDF_DIR + nome_arquivo, 'rb') as arquivo_pdf:
            response = HttpResponse(arquivo_pdf, content_type='application/pdf')
            #  response['Content-Disposition'] = 'attachment; filename=%s' % smart_str(nome_arquivo) # janela de download
            response['Content-Disposition'] = 'inline; filename=%s' % smart_str(nome_arquivo) # abre no visualizador de PDF do navegador
            #  response['X-Sendfile'] = PDF_DIR + nome_arquivo

            return response


class DeletarRelatorio(LoginRequiredMixin, View):
    def post(self, request):
        relatorio = get_object_or_404(Relatorio, pk=request.POST['pk'])
        if relatorio.projeto_extensao.user == request.user:
            relatorio.delete()
            return redirect('relatorio:consulta', relatorio.projeto_extensao.pk)
        else:
            return redirect('base:index') #TODO: mensagem de erro
