from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View, generic

from base.models import Docente
from .forms import DocenteForm

class NovoDocente(LoginRequiredMixin, View):
    def get(self, request):
        main_form = DocenteForm(prefix='main')

        return render(request, 'docente/docente_form.html', {'main_form': main_form})

    def post(self, request):
        main_form = DocenteForm(request.POST, prefix='main')

        docente = main_form.instance

        if main_form.is_valid():
            with transaction.atomic():
                main_form.save()

            return redirect('curso_extensao:index')

        else:
            return render(request, 'docente/docente_form.html', {'main_form': main_form})


class ConsultaDocente(LoginRequiredMixin, generic.ListView):
    model = Docente

    def get_queryset(self):
        d = {}
        if 'nome_completo' in self.request.GET:
            d['nome_completo__contains'] = self.request.GET.get('nome_completo', '')
            d['email__contains'] = self.request.GET.get('email', '')

        return Docente.objects.filter(**d)


class DetalheDocente(LoginRequiredMixin, View):
    def get(self, request, pk):
        docente = get_object_or_404(Docente, pk=pk)

        main_form = DocenteForm(instance=docente, prefix='main')

        return render(request, 'docente/docente_form.html', {'main_form': main_form})

    def post(self, request, pk):
        docente = get_object_or_404(Docente, pk=pk)

        main_form = DocenteForm(request.POST, instance=docente, prefix='main')

        docente = main_form.instance

        if main_form.is_valid():
            with transaction.atomic():
                main_form.save()

            return redirect('curso_extensao:index')

        else:
            return render(request, 'docente/docente_form.html', {'main_form': main_form})
