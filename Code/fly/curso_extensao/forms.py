from django import forms
from django.forms.models import inlineformset_factory


from .models import CursoExtensao, Servidor_CursoExtensao, PalavraChave_CursoExtensao, Discente_CursoExtensao, MembroComunidade_CursoExtensao


class CursoExtensaoForm(forms.ModelForm):
    class Meta:
        model = CursoExtensao
        fields = ['titulo', 'coordenador', 'periodo_de_realizacao', 'programa_extensao', 'unidade_administrativa', 'campus', 'centro', 'grande_area', 'area_tematica_principal', 'area_tematica_secundaria', 'linha_extensao', 'publico_alvo', 'numero_pessoas_beneficiadas', 'carga_horaria_total', 'numero_vagas', 'local_inscricao', 'resumo', 'programacao', 'previsao_orcamentaria']


Servidor_CursoExtensaoFormSet = inlineformset_factory(CursoExtensao, Servidor_CursoExtensao, extra=2, fields=['servidor', 'carga_horaria_dedicada', 'funcao'])
PalavraChave_CursoExtensaoFormSet = inlineformset_factory(CursoExtensao, PalavraChave_CursoExtensao, extra=3, min_num=1, max_num=3, fields=['nome'])
Discente_CursoExtensaoFormSet = inlineformset_factory(CursoExtensao, Discente_CursoExtensao, extra=2, fields=['nome', 'curso', 'serie', 'turno', 'carga_horaria_semanal', 'telefone', 'email'])
MembroComunidade_CursoExtensaoFormSet = inlineformset_factory(CursoExtensao, MembroComunidade_CursoExtensao, extra=2, fields=['nome', 'carga_horaria_semanal', 'entidade', 'telefone', 'email', 'cpf', 'data_nascimento', 'funcao'])
