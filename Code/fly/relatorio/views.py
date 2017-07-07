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


class ListaRelatorio(generic.ListView):
    pass

class DetalheRelatorio(generic.DetailView):
    pass
