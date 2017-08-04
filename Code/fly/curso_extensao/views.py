# -*- coding: utf-8 -*-

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.db.models import F
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.utils.encoding import smart_str
from django.views import View, generic
from fly.settings import PDF_DIR

from .forms import CursoExtensaoForm, AgenteUniversitario_CursoExtensaoFormSet, Docente_CursoExtensaoFormSet, PalavraChave_CursoExtensaoFormSet, Discente_CursoExtensaoFormSet, MembroComunidade_CursoExtensaoFormSet, PrevisaoOrcamentaria_CursoExtensaoFormSet
from .models import CursoExtensao
from base.models import EstadoProjeto
from curso_extensao.pdfs import gerar_pdf

import subprocess

def validar_curso_extensao(main_form, palavras_formset, discentes_formset, docentes_formset, agentes_universitarios_formset, membros_comunidade_formset, previsao_orcamentaria_formset):
    coordenador = False
    subcoordenador = False

    # Não permitir mais de 1 coordenador e mais de 1 subcoordenador

    for formset in [docentes_formset, agentes_universitarios_formset]:
        formset.clean()
        for form in formset.forms:
            if form.cleaned_data and not form.cleaned_data.get('DELETE', False):
                funcao = form.cleaned_data.get('funcao')
                if funcao:
                    if funcao.nome == 'Coordenador(a)':
                        if coordenador:
                            form.add_error('funcao', "Somente um coordenador é permitido.")
                        coordenador = True
                    elif funcao.nome == 'Subcoordenador(a)':
                        if subcoordenador:
                            form.add_error('funcao', "Somente um subcoordenador é permitido.")
                        subcoordenador = True

    # Não permitir nenhum coordenador

    if not coordenador:
        main_form.add_error(None, "É necessário ter um coordenador.")

class NovoCursoExtensao(LoginRequiredMixin, View):
    def get(self, request):
        # Initialize empty forms and formsets.
        main_form = CursoExtensaoForm(prefix='main')
        palavras_formset = PalavraChave_CursoExtensaoFormSet(prefix='palavras')
        discentes_formset = Discente_CursoExtensaoFormSet(prefix='discentes')
        docentes_formset = Docente_CursoExtensaoFormSet(prefix='docentes')
        agentes_universitarios_formset = AgenteUniversitario_CursoExtensaoFormSet(prefix='agentes_universitarios')
        membros_comunidade_formset = MembroComunidade_CursoExtensaoFormSet(prefix='membros')
        previsao_orcamentaria_formset = PrevisaoOrcamentaria_CursoExtensaoFormSet(prefix='previsao')

        palavras_formset.can_delete = False
        discentes_formset.can_delete = False
        docentes_formset.can_delete = False
        agentes_universitarios_formset.can_delete = False
        membros_comunidade_formset.can_delete = False
        previsao_orcamentaria_formset.can_delete = False

        return render(request, 'curso_extensao/cursoextensao_form.html', {'main_form': main_form, 'docentes_formset': docentes_formset, 'agentes_universitarios_formset': agentes_universitarios_formset, 'palavras_formset': palavras_formset, 'discentes_formset': discentes_formset, 'membros_comunidade_formset': membros_comunidade_formset, 'previsao_orcamentaria_formset': previsao_orcamentaria_formset})

    def post(self, request):
        # Initialize form with POST data.
        main_form = CursoExtensaoForm(request.POST, prefix='main')

        curso_extensao = main_form.instance

        # Initialize formsets with POST data and foreignKey already set.
        palavras_formset = PalavraChave_CursoExtensaoFormSet(request.POST, instance=curso_extensao, prefix='palavras')
        discentes_formset = Discente_CursoExtensaoFormSet(request.POST, instance=curso_extensao, prefix='discentes')
        docentes_formset = Docente_CursoExtensaoFormSet(request.POST, instance=curso_extensao, prefix='docentes')
        agentes_universitarios_formset = AgenteUniversitario_CursoExtensaoFormSet(request.POST, instance=curso_extensao, prefix='agentes_universitarios')
        membros_comunidade_formset = MembroComunidade_CursoExtensaoFormSet(request.POST, instance=curso_extensao, prefix='membros')
        previsao_orcamentaria_formset = PrevisaoOrcamentaria_CursoExtensaoFormSet(request.POST, instance=curso_extensao, prefix='previsao')

        validar_curso_extensao(main_form, palavras_formset, discentes_formset, docentes_formset, agentes_universitarios_formset, membros_comunidade_formset, previsao_orcamentaria_formset)

        if (main_form.is_valid()
                and palavras_formset.is_valid()
                and discentes_formset.is_valid()
                and docentes_formset.is_valid()
                and agentes_universitarios_formset.is_valid()
                and membros_comunidade_formset.is_valid()
                and previsao_orcamentaria_formset.is_valid()):

            # Set extra data
            curso_extensao.user = request.user
            curso_extensao.data = timezone.now()
            curso_extensao.estado = EstadoProjeto.objects.get(nome='Não submetido')

            with transaction.atomic():
                main_form.save()
                palavras_formset.save()
                discentes_formset.save()
                docentes_formset.save()
                agentes_universitarios_formset.save()
                membros_comunidade_formset.save()
                previsao_orcamentaria_formset.save()

            return redirect('curso_extensao:consulta')
        else:
            palavras_formset.can_delete = False
            discentes_formset.can_delete = False
            docentes_formset.can_delete = False
            agentes_universitarios_formset.can_delete = False
            membros_comunidade_formset.can_delete = False
            previsao_orcamentaria_formset.can_delete = False

            return render(request, 'curso_extensao/cursoextensao_form.html', {'main_form': main_form, 'docentes_formset': docentes_formset, 'agentes_universitarios_formset': agentes_universitarios_formset, 'palavras_formset': palavras_formset, 'discentes_formset': discentes_formset, 'membros_comunidade_formset': membros_comunidade_formset, 'previsao_orcamentaria_formset': previsao_orcamentaria_formset})


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
        docentes_formset = Docente_CursoExtensaoFormSet(instance=curso_extensao, prefix='docentes')
        agentes_universitarios_formset = AgenteUniversitario_CursoExtensaoFormSet(instance=curso_extensao, prefix='agentes_universitarios')
        membros_comunidade_formset = MembroComunidade_CursoExtensaoFormSet(instance=curso_extensao, prefix='membros')
        previsao_orcamentaria_formset = PrevisaoOrcamentaria_CursoExtensaoFormSet(instance=curso_extensao, prefix='previsao')

        return render(request, 'curso_extensao/cursoextensao_form.html', {'main_form': main_form, 'docentes_formset': docentes_formset, 'agentes_universitarios_formset': agentes_universitarios_formset, 'palavras_formset': palavras_formset, 'discentes_formset': discentes_formset, 'membros_comunidade_formset': membros_comunidade_formset, 'previsao_orcamentaria_formset': previsao_orcamentaria_formset})

    def post(self, request, pk):
        curso_extensao = get_object_or_404(CursoExtensao, pk=pk)

        # Initialize form with POST data.
        main_form = CursoExtensaoForm(request.POST, instance=curso_extensao, prefix='main')

        curso_extensao = main_form.instance

        # Initialize formsets with POST data and foreignKey already set.
        palavras_formset = PalavraChave_CursoExtensaoFormSet(request.POST, instance=curso_extensao, prefix='palavras')
        discentes_formset = Discente_CursoExtensaoFormSet(request.POST, instance=curso_extensao, prefix='discentes')
        docentes_formset = Docente_CursoExtensaoFormSet(request.POST, instance=curso_extensao, prefix='docentes')
        agentes_universitarios_formset = AgenteUniversitario_CursoExtensaoFormSet(request.POST, instance=curso_extensao, prefix='agentes_universitarios')
        membros_comunidade_formset = MembroComunidade_CursoExtensaoFormSet(request.POST, instance=curso_extensao, prefix='membros')
        previsao_orcamentaria_formset = PrevisaoOrcamentaria_CursoExtensaoFormSet(request.POST, instance=curso_extensao, prefix='previsao')

        #TODO:
        if curso_extensao.estado.nome == 'B':
            main_form.add_error(None, "Não é possível editar esse curso de extensão, pois ele já foi submetido.")

        validar_curso_extensao(main_form, palavras_formset, discentes_formset, docentes_formset, agentes_universitarios_formset, membros_comunidade_formset, previsao_orcamentaria_formset)

        if (main_form.is_valid()
                and palavras_formset.is_valid()
                and discentes_formset.is_valid()
                and docentes_formset.is_valid()
                and agentes_universitarios_formset.is_valid()
                and membros_comunidade_formset.is_valid()
                and previsao_orcamentaria_formset.is_valid()):

            # Set extra data
            curso_extensao.user = request.user
            curso_extensao.data = timezone.now()

            with transaction.atomic():
                main_form.save()
                palavras_formset.save()
                discentes_formset.save()
                docentes_formset.save()
                agentes_universitarios_formset.save()
                membros_comunidade_formset.save()
                previsao_orcamentaria_formset.save()

            return redirect('curso_extensao:consulta')
        else:
            return render(request, 'curso_extensao/cursoextensao_form.html', {'main_form': main_form, 'docentes_formset': docentes_formset, 'agentes_universitarios_formset': agentes_universitarios_formset, 'palavras_formset': palavras_formset, 'discentes_formset': discentes_formset, 'membros_comunidade_formset': membros_comunidade_formset, 'previsao_orcamentaria_formset': previsao_orcamentaria_formset})


class GeracaoPDFCursoExtensao(LoginRequiredMixin, View):
    def get(self, request, pk):
        curso_extensao = get_object_or_404(CursoExtensao, pk=pk)

        # TODO:
        #  try:
        gerar_pdf(curso_extensao)
        #  except subprocess.CalledProcessError:
            #  pass

        nome_arquivo = 'curso_extensao_{}.pdf'.format(str(pk))

        with open(PDF_DIR + nome_arquivo, 'rb') as arquivo_pdf:
            response = HttpResponse(arquivo_pdf, content_type='application/pdf')
            #  response['Content-Disposition'] = 'attachment; filename=%s' % smart_str(nome_arquivo) # janela de download
            response['Content-Disposition'] = 'inline; filename=%s' % smart_str(nome_arquivo) # abre no visualizador de PDF do navegador
            #  response['X-Sendfile'] = PDF_DIR + nome_arquivo

            return response


class DeletarCursoExtensao(LoginRequiredMixin, View):
    def post(self, request):
        curso_extensao = get_object_or_404(CursoExtensao, pk=request.POST['pk'])
        if curso_extensao.user == request.user:
            curso_extensao.delete()
            return redirect('curso_extensao:consulta')
        else:
            return redirect('curso_extensao:consulta') #TODO: mensagem de erro
