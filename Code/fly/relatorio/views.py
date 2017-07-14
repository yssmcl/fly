from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View, generic

from curso_extensao.models import CursoExtensao
from .forms import RelatorioForm, CertificadoRelatorioFormSet
from .models import Relatorio

class NovoRelatorio(View):
    def get(self, request, pk):
        main_form = RelatorioForm(prefix='main')
        certificados_formset = CertificadoRelatorioFormSet(prefix='certificados')

        projeto_extensao = get_object_or_404(CursoExtensao, pk=pk)

        return render(request, 'relatorio/relatorio_form.html', {'main_form': main_form, 'certificados_formset': certificados_formset, 'projeto_extensao': projeto_extensao})

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
            return render(request, 'relatorio/relatorio_form.html', {'main_form': main_form, 'certificados_formset': certificados_formset, 'projeto_extensao': relatorio.projeto_extensao})


class ConsultaRelatorio(LoginRequiredMixin, generic.ListView):
    model = Relatorio

    def get_queryset(self):
        d = {}
        if 'projeto_extensao' in self.request.GET:
            d['projeto_extensao__contains'] = self.request.GET.get('projeto_extensao', '')
            d['coordenador__contains'] = self.request.GET.get('coordenador', '')
            d['periodo_inicio__contains'] = self.request.GET.get('periodo_inicio', '')
            d['periodo_fim__contains'] = self.request.GET.get('periodo_fim', '')

        return Relatorio.objects.filter(**d)


class DetalheRelatorio(LoginRequiredMixin, View):
    def get(self, request, pk):
        relatorio = get_object_or_404(Relatorio, pk=pk)

        main_form = RelatorioForm(instance=relatorio, prefix='main')

        return render(request, 'relatorio/relatorio_form.html', {'main_form': main_form})

    def post(self, request, pk):
        relatorio = get_object_or_404(Relatorio, pk=pk)

        main_form = RelatorioForm(request.POST, instance=relatorio, prefix='main')

        relatorio = main_form.instance

        if main_form.is_valid():
            with transaction.atomic():
                main_form.save()

            return redirect('curso_extensao:index')

        else:
            return render(request, 'relatorio/relatorio_form.html', {'main_form': main_form})
