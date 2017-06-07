from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import F
from django.views import View, generic
from django.utils import timezone
from django.db import transaction

from .models import CursoExtensao
from .forms import CursoExtensaoForm, Servidor_CursoExtensaoFormSet, PalavraChave_CursoExtensaoFormSet, Discente_CursoExtensaoFormSet, MembroComunidade_CursoExtensaoFormSet


class IndexView(View):
    def get(self, request):
        return render(request, 'curso_extensao/index.html', {})


class NovoCursoExtensao(LoginRequiredMixin, View):
    def get(self, request):
        # Initialize empty forms and formsets.
        main_form = CursoExtensaoForm(prefix='main')
        palavras_form = PalavraChave_CursoExtensaoFormSet(prefix='palavras')
        discentes_form = Discente_CursoExtensaoFormSet(prefix='discentes')
        servidores_form = Servidor_CursoExtensaoFormSet(prefix='servidores')
        membros_comunidade_form = MembroComunidade_CursoExtensaoFormSet(prefix='membros')

        palavras_form.can_delete = False
        discentes_form.can_delete = False
        servidores_form.can_delete = False
        membros_comunidade_form.can_delete = False

        return render(request, 'curso_extensao/cursoextensao_form.html', {'main_form': main_form, 'servidores_form': servidores_form, 'palavras_form': palavras_form, 'discentes_form': discentes_form, 'membros_comunidade_form': membros_comunidade_form})

    def post(self, request):
        # Initialize form with POST data.
        main_form = CursoExtensaoForm(request.POST, prefix='main')

        curso_extensao = main_form.instance

        # Initialize formsets with POST data and foreignKey already set.
        discentes_form = Discente_CursoExtensaoFormSet(request.POST, instance=curso_extensao, prefix='discentes')
        servidores_form = Servidor_CursoExtensaoFormSet(request.POST, instance=curso_extensao, prefix='servidores')
        palavras_form = PalavraChave_CursoExtensaoFormSet(request.POST, instance=curso_extensao, prefix='palavras')
        membros_comunidade_form = MembroComunidade_CursoExtensaoFormSet(request.POST, instance=curso_extensao, prefix='membros')

        if (main_form.is_valid()
                and servidores_form.is_valid()
                and palavras_form.is_valid()
                and discentes_form.is_valid()
                and membros_comunidade_form.is_valid()):

            # Set extra data
            curso_extensao.user = request.user
            curso_extensao.data = timezone.now()

            with transaction.atomic():
                main_form.save()
                palavras_form.save()
                discentes_form.save()
                servidores_form.save()
                membros_comunidade_form.save()

            return redirect('curso_extensao:index')
        else:
            palavras_form.can_delete = False
            discentes_form.can_delete = False
            servidores_form.can_delete = False
            membros_comunidade_form.can_delete = False

            return render(request, 'curso_extensao/cursoextensao_form.html', {'main_form': main_form, 'servidores_form': servidores_form, 'palavras_form': palavras_form, 'discentes_form': discentes_form, 'membros_comunidade_form': membros_comunidade_form})

class ConsultaCursoExtensao(LoginRequiredMixin, View):
    def get(self, request):
        #  pk = request.POST['curso_extensao']
        curso_extensao = CursoExtensao.objects.get(pk=pk)
        main_form = CursoExtensaoForm(instance=curso_extensao, prefix='main')

        return render(request, 'curso_extensao/cursoextensao_form.html', {'main_form': main_form})

    def post(self, request):
        # Initialize form with POST data.
        main_form = CursoExtensaoForm(request.POST, prefix='main')

        curso_extensao = main_form.instance

        # Initialize formsets with POST data and foreignKey already set.
        discentes_form = Discente_CursoExtensaoFormSet(request.POST, instance=curso_extensao, prefix='discentes')
        servidores_form = Servidor_CursoExtensaoFormSet(request.POST, instance=curso_extensao, prefix='servidores')
        palavras_form = PalavraChave_CursoExtensaoFormSet(request.POST, instance=curso_extensao, prefix='palavras')
        membros_comunidade_form = MembroComunidade_CursoExtensaoFormSet(request.POST, instance=curso_extensao, prefix='membros')

        if (main_form.is_valid()
                and servidores_form.is_valid()
                and palavras_form.is_valid()
                and discentes_form.is_valid()
                and membros_comunidade_form.is_valid()):

            # Set extra data
            curso_extensao.user = request.user
            curso_extensao.data = timezone.now()

            with transaction.atomic():
                main_form.save()
                palavras_form.save()
                discentes_form.save()
                servidores_form.save()
                membros_comunidade_form.save()

            return redirect('curso_extensao:index')
        else:
            return render(request, 'curso_extensao/cursoextensao_form.html', {'main_form': main_form, 'servidores_form': servidores_form, 'palavras_form': palavras_form, 'discentes_form': discentes_form, 'membros_comunidade_form': membros_comunidade_form})
