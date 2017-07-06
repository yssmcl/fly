from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import F
from django.views import View, generic
from django.utils import timezone
from django.db import transaction

from .models import CursoExtensao
from .forms import CursoExtensaoForm, Servidor_CursoExtensaoFormSet, PalavraChave_CursoExtensaoFormSet, Discente_CursoExtensaoFormSet, MembroComunidade_CursoExtensaoFormSet, PrevisaoOrcamentaria_CursoExtensaoFormSet
from base.models import EstadoProjeto
from curso_extensao.pdf.geracaopdf import gerar_pdf


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
        previsao_orcamentaria_formset = PrevisaoOrcamentaria_CursoExtensaoFormSet(prefix='previsao')

        palavras_formset.can_delete = False
        discentes_formset.can_delete = False
        servidores_formset.can_delete = False
        membros_comunidade_formset.can_delete = False
        previsao_orcamentaria_formset.can_delete = False

        return render(request, 'curso_extensao/cursoextensao_form.html', {'main_form': main_form, 'servidores_formset': servidores_formset, 'palavras_formset': palavras_formset, 'discentes_formset': discentes_formset, 'membros_comunidade_formset': membros_comunidade_formset, 'previsao_orcamentaria_formset': previsao_orcamentaria_formset})

    def post(self, request):
        # Initialize form with POST data.
        main_form = CursoExtensaoForm(request.POST, prefix='main')

        curso_extensao = main_form.instance

        # Initialize formsets with POST data and foreignKey already set.
        palavras_formset = PalavraChave_CursoExtensaoFormSet(request.POST, instance=curso_extensao, prefix='palavras')
        discentes_formset = Discente_CursoExtensaoFormSet(request.POST, instance=curso_extensao, prefix='discentes')
        servidores_formset = Servidor_CursoExtensaoFormSet(request.POST, instance=curso_extensao, prefix='servidores')
        membros_comunidade_formset = MembroComunidade_CursoExtensaoFormSet(request.POST, instance=curso_extensao, prefix='membros')
        previsao_orcamentaria_formset = PrevisaoOrcamentaria_CursoExtensaoFormSet(request.POST, instance=curso_extensao, prefix='previsao')

        if (main_form.is_valid()
                and palavras_formset.is_valid()
                and discentes_formset.is_valid()
                and servidores_formset.is_valid()
                and membros_comunidade_formset.is_valid()
                and previsao_orcamentaria_formset.is_valid()):

            # Set extra data
            curso_extensao.user = request.user
            curso_extensao.data = timezone.now()
            curso_extensao.estado = EstadoProjeto.objects.get(nome='A') #TODO:

            with transaction.atomic():
                main_form.save()
                palavras_formset.save()
                discentes_formset.save()
                servidores_formset.save()
                membros_comunidade_formset.save()
                previsao_orcamentaria_formset.save()

            return redirect('curso_extensao:index')
        else:
            palavras_formset.can_delete = False
            discentes_formset.can_delete = False
            servidores_formset.can_delete = False
            membros_comunidade_formset.can_delete = False
            previsao_orcamentaria_formset.can_delete = False

            return render(request, 'curso_extensao/cursoextensao_form.html', {'main_form': main_form, 'servidores_formset': servidores_formset, 'palavras_formset': palavras_formset, 'discentes_formset': discentes_formset, 'membros_comunidade_formset': membros_comunidade_formset, 'previsao_orcamentaria_formset': previsao_orcamentaria_formset})


class ConsultaCursoExtensao(LoginRequiredMixin, generic.ListView):
    model = CursoExtensao        

    def get_queryset(self):
        d = { 'user': self.request.user }

        if 'titulo' in self.request.GET:
            d['titulo__contains'] = self.request.GET.get('titulo', '')

        if 'coordenador' in self.request.GET:
            d['coordenador__nome_completo__contains'] = self.request.GET.get('coordenador', '')

        if 'estado' in self.request.GET:
            d['estado__nome__contains'] = self.request.GET.get('estado', '')

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
        previsao_orcamentaria_formset = PrevisaoOrcamentaria_CursoExtensaoFormSet(instance=curso_extensao, prefix='previsao')

        return render(request, 'curso_extensao/cursoextensao_form.html', {'main_form': main_form, 'servidores_formset': servidores_formset, 'palavras_formset': palavras_formset, 'discentes_formset': discentes_formset, 'membros_comunidade_formset': membros_comunidade_formset, 'previsao_orcamentaria_formset': previsao_orcamentaria_formset})

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
        previsao_orcamentaria_formset = PrevisaoOrcamentaria_CursoExtensaoFormSet(request.POST, instance=curso_extensao, prefix='previsao')

        #TODO:
        if curso_extensao.estado.nome == 'B':
            main_form.add_error(None, "Não é possível editar esse curso de extensão pois ele já foi submetido.")

        if (main_form.is_valid()
                and palavras_formset.is_valid()
                and discentes_formset.is_valid()
                and servidores_formset.is_valid()
                and membros_comunidade_formset.is_valid()
                and previsao_orcamentaria_formset.is_valid()):

            # Set extra data
            curso_extensao.user = request.user
            curso_extensao.data = timezone.now()

            with transaction.atomic():
                main_form.save()
                palavras_formset.save()
                discentes_formset.save()
                servidores_formset.save()
                membros_comunidade_formset.save()
                previsao_orcamentaria_formset.save()

            return redirect('curso_extensao:index')
        else:
            return render(request, 'curso_extensao/cursoextensao_form.html', {'main_form': main_form, 'servidores_formset': servidores_formset, 'palavras_formset': palavras_formset, 'discentes_formset': discentes_formset, 'membros_comunidade_formset': membros_comunidade_formset, 'previsao_orcamentaria_formset': previsao_orcamentaria_formset})


class GeracaoPDFCursoExtensao(LoginRequiredMixin, View):
    def get(self, request, pk):
        curso_extensao = get_object_or_404(CursoExtensao, pk=pk)
        gerar_pdf(curso_extensao)
        return render(request, 'curso_extensao/index.html')
