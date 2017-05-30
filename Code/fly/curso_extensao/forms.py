# from django.forms import ModelForm
# from django.forms.models import inlineformset_factory

# from .models import CursoExtensao, PrevisaoOrcamentaria

# class CursoExtensaoForm(ModelForm):
#     fields = ['titulo','coordenador','periodo_de_realizacao','programa_extensao','unidade_administrativa','campus','centro','grande_area','area_tematica_principal','area_tematica_secundaria','linha_extensao','publico_alvo','numero_pessoas_beneficiadas','carga_horaria_total','numero_vagas','local_inscricao','resumo','programacao','servidores','previsao_orcamentaria']
#     class Meta:
#         fields = ['titulo','coordenador','periodo_de_realizacao','programa_extensao','unidade_administrativa','campus','centro','grande_area','area_tematica_principal','area_tematica_secundaria','linha_extensao','publico_alvo','numero_pessoas_beneficiadas','carga_horaria_total','numero_vagas','local_inscricao','resumo','programacao','servidores','previsao_orcamentaria']
#         model = CursoExtensao


# PrevisaoOrcamentariaFormSet = inlineformset_factory(CursoExtensaoForm, PrevisaoOrcamentaria)