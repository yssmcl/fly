from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import F
from django.views import View, generic

from .models import CursoExtensao
# from .forms import CursoExtensaoForm, PrevisaoOrcamentariaFormSet

class IndexView(View):
    def get(self, request):
        return render(request, 'curso_extensao/index.html', {})

class NovoCursoExtensao(LoginRequiredMixin, generic.CreateView):
    model = CursoExtensao
    fields = ['titulo','coordenador','periodo_de_realizacao','programa_extensao','unidade_administrativa','campus','centro','grande_area','area_tematica_principal','area_tematica_secundaria','linha_extensao','publico_alvo','numero_pessoas_beneficiadas','carga_horaria_total','numero_vagas','local_inscricao','resumo','programacao','previsao_orcamentaria']
