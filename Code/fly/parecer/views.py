from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View, generic

from curso_extensao.models import CursoExtensao
from .models import Parecer
from .forms import ParecerForm

class NovoParecer(View):
    def get(self, request, pk):
        form = ParecerForm()

        projeto_extensao = get_object_or_404(CursoExtensao, pk=pk)

        return render(request, 'parecer/parecer_form.html', {'form': form, 'projeto_extensao': projeto_extensao})

    def post(self, request, pk):
        form = ParecerForm(request.POST)

        parecer = form.instance

        parecer.projeto_extensao = get_object_or_404(CursoExtensao, pk=pk)

        if form.is_valid():
            form.save()

            return redirect('base:index')
        else:
            return render(request, 'parecer/parecer_form.html', {'form': form, 'projeto_extensao': parecer.projeto_extensao})

class DetalheParecer(LoginRequiredMixin, View):
    def get(self, request, pk):
        parecer = get_object_or_404(Parecer, pk=pk)

        main_form = ParecerForm(instance=parecer, prefix='main')

        return render(request, 'parecer/parecer_form.html', {'main_form': main_form})

    def post(self, request, pk):
        parecer = get_object_or_404(parecer, pk=pk)

        main_form = ParecerForm(request.POST, instance=parecer, prefix='main')

        parecer = main_form.instance

        if main_form.is_valid():
            with transaction.atomic():
                main_form.save()

            return redirect('base:index')

        else:
            return render(request, 'parecer/parecer_form.html', {'main_form': main_form})
