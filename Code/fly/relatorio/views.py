from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View, generic

from curso_extensao.models import CursoExtensao
from .models import Relatorio
from .forms import RelatorioForm

class NovoRelatorio(View):
    def get(self, request, pk):
        form = RelatorioForm()

        projeto_extensao = get_object_or_404(CursoExtensao, pk=pk)

        return render(request, 'relatorio/relatorio_form.html', {'form': form, 'projeto_extensao': projeto_extensao})

    def post(self, request, pk):
        form = RelatorioForm(request.POST)

        relatorio = form.instance

        relatorio.projeto_extensao = get_object_or_404(CursoExtensao, pk=pk)

        if form.is_valid():
            form.save()

            return redirect('curso_extensao:index')
        else:
            return render(request, 'relatorio/relatorio_form.html', {'form': form, 'projeto_extensao': relatorio.projeto_extensao})


class ListaRelatorio(generic.ListView):
    pass

class DetalheRelatorio(generic.DetailView):
    pass
