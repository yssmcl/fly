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
        return render(request, 'curso_extensao/index.html')


class NovoCursoExtensao(LoginRequiredMixin, View):
    def get(self, request):
        # Initialize empty forms and formsets.
        main_form = CursoExtensaoForm(prefix='main')
        palavras_formset = PalavraChave_CursoExtensaoFormSet(prefix='palavras')
        discentes_formset = Discente_CursoExtensaoFormSet(prefix='discentes')
        servidores_formset = Servidor_CursoExtensaoFormSet(prefix='servidores')
        membros_comunidade_formset = MembroComunidade_CursoExtensaoFormSet(prefix='membros')

        palavras_formset.can_delete = False
        discentes_formset.can_delete = False
        servidores_formset.can_delete = False
        membros_comunidade_formset.can_delete = False

        # s = []

        # # for form in palavras_formset:
        # for field in main_form:
        #     s.append(str(field)) 
        # # break

        # return render(request, 'debug.html', {'value':'|||||||||'.join(s)})

        return render(request, 'curso_extensao/cursoextensao_form.html', {'main_form': main_form, 'servidores_formset': servidores_formset, 'palavras_formset': palavras_formset, 'discentes_formset': discentes_formset, 'membros_comunidade_formset': membros_comunidade_formset})

    def post(self, request):
        # Initialize form with POST data.
        main_form = CursoExtensaoForm(request.POST, prefix='main')

        curso_extensao = main_form.instance

        # Initialize formsets with POST data and foreignKey already set.
        palavras_formset = PalavraChave_CursoExtensaoFormSet(request.POST, instance=curso_extensao, prefix='palavras')
        discentes_formset = Discente_CursoExtensaoFormSet(request.POST, instance=curso_extensao, prefix='discentes')
        servidores_formset = Servidor_CursoExtensaoFormSet(request.POST, instance=curso_extensao, prefix='servidores')
        membros_comunidade_formset = MembroComunidade_CursoExtensaoFormSet(request.POST, instance=curso_extensao, prefix='membros')

        if (main_form.is_valid()
                and palavras_formset.is_valid()
                and discentes_formset.is_valid()
                and servidores_formset.is_valid()
                and membros_comunidade_formset.is_valid()):

            # Set extra data
            curso_extensao.user = request.user
            curso_extensao.data = timezone.now()

            with transaction.atomic():
                main_form.save()
                palavras_formset.save()
                discentes_formset.save()
                servidores_formset.save()
                membros_comunidade_formset.save()

            return redirect('curso_extensao:index')
        else:
            palavras_formset.can_delete = False
            discentes_formset.can_delete = False
            servidores_formset.can_delete = False
            membros_comunidade_formset.can_delete = False

            return render(request, 'curso_extensao/cursoextensao_form.html', {'main_form': main_form, 'servidores_formset': servidores_formset, 'palavras_formset': palavras_formset, 'discentes_formset': discentes_formset, 'membros_comunidade_formset': membros_comunidade_formset})


class ConsultaCursoExtensao(LoginRequiredMixin, generic.ListView):
    model = CursoExtensao        

    def get_queryset(self):
        d = {
            'user':self.request.user,
            'titulo__contains':self.request.GET.get('titulo', '')
        }

        return CursoExtensao.objects.filter(**d)

class DetalheCursoExtensao(LoginRequiredMixin, View):
    def get(self, request, pk):
        curso_extensao = get_object_or_404(CursoExtensao, pk=pk)

        # Initialize empty forms and formsets.
        main_form = CursoExtensaoForm(instance=curso_extensao, prefix='main')
        palavras_formset = PalavraChave_CursoExtensaoFormSet(instance=curso_extensao, prefix='palavras')
        discentes_formset = Discente_CursoExtensaoFormSet(instance=curso_extensao, prefix='discentes')
        servidores_formset = Servidor_CursoExtensaoFormSet(instance=curso_extensao, prefix='servidores')
        membros_comunidade_formset = MembroComunidade_CursoExtensaoFormSet(instance=curso_extensao, prefix='membros')

        return render(request, 'curso_extensao/cursoextensao_form.html', {'main_form': main_form, 'servidores_formset': servidores_formset, 'palavras_formset': palavras_formset, 'discentes_formset': discentes_formset, 'membros_comunidade_formset': membros_comunidade_formset})

    def post(self, request, pk):
        curso_extensao = get_object_or_404(CursoExtensao, pk=pk)

        # Initialize form with POST data.
        main_form = CursoExtensaoForm(request.POST, instance=curso_extensao, prefix='main')

        curso_extensao = main_form.instance

        # Initialize formsets with POST data and foreignKey already set.
        palavras_formset = PalavraChave_CursoExtensaoFormSet(request.POST, instance=curso_extensao, prefix='palavras')
        discentes_formset = Discente_CursoExtensaoFormSet(request.POST, instance=curso_extensao, prefix='discentes')
        servidores_formset = Servidor_CursoExtensaoFormSet(request.POST, instance=curso_extensao, prefix='servidores')
        membros_comunidade_formset = MembroComunidade_CursoExtensaoFormSet(request.POST, instance=curso_extensao, prefix='membros')

        if (main_form.is_valid()
                and palavras_formset.is_valid()
                and discentes_formset.is_valid()
                and servidores_formset.is_valid()
                and membros_comunidade_formset.is_valid()):

            # Set extra data
            curso_extensao.user = request.user
            curso_extensao.data = timezone.now()

            with transaction.atomic():
                main_form.save()
                palavras_formset.save()
                discentes_formset.save()
                servidores_formset.save()
                membros_comunidade_formset.save()

            return redirect('curso_extensao:index')
        else:
            return render(request, 'curso_extensao/cursoextensao_form.html', {'main_form': main_form, 'servidores_formset': servidores_formset, 'palavras_formset': palavras_formset, 'discentes_formset': discentes_formset, 'membros_comunidade_formset': membros_comunidade_formset})