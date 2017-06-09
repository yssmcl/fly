from django import forms

from .models import CursoExtensao, Servidor_CursoExtensao, PalavraChave_CursoExtensao, Discente_CursoExtensao, MembroComunidade_CursoExtensao, PrevisaoOrcamentaria_CursoExtensao

from django.utils.translation import ugettext_lazy as _

class CursoExtensaoForm(forms.ModelForm):
    class Meta:
        model = CursoExtensao
        fields = ['titulo', 'coordenador', 'periodo_realizacao_inicio', 'periodo_realizacao_fim', 'programa_extensao', 'unidade_administrativa', 'campus', 'centro', 'grande_area', 'area_tematica_principal', 'area_tematica_secundaria', 'linha_extensao', 'publico_alvo', 'numero_pessoas_beneficiadas', 'carga_horaria_total', 'numero_vagas', 'local_inscricao', 'resumo', 'programacao']

    resumo = forms.CharField(max_length=CursoExtensao._meta.get_field('resumo').max_length, widget=forms.Textarea)
    programacao = forms.CharField(max_length=CursoExtensao._meta.get_field('programacao').max_length, widget=forms.Textarea)

    def clean(self):
        cleaned_data = super(CursoExtensaoForm, self).clean()

        # Obrigar existir pelo menos 1 dos 2, mas não os 2 ao mesmo tempo.
        unidade_administrativa = cleaned_data.get('unidade_administrativa')
        campus = cleaned_data.get('campus')

        if unidade_administrativa and campus:
            error = "Preencher somente um."
            self.add_error('unidade_administrativa', error)
            self.add_error('campus', error)
        if not unidade_administrativa and not campus:
            error = _("This field is required.")
            self.add_error('unidade_administrativa', error)
            self.add_error('campus', error)


Servidor_CursoExtensaoFormSet = forms.models.inlineformset_factory(CursoExtensao, Servidor_CursoExtensao, extra=1, fields=['servidor', 'carga_horaria_dedicada', 'funcao'])
Discente_CursoExtensaoFormSet = forms.models.inlineformset_factory(CursoExtensao, Discente_CursoExtensao, extra=1, fields=['nome', 'curso', 'serie', 'turno', 'carga_horaria_semanal', 'telefone', 'email'])
PalavraChave_CursoExtensaoFormSet = forms.models.inlineformset_factory(CursoExtensao, PalavraChave_CursoExtensao, extra=3, min_num=1, max_num=3, fields=['nome'])
MembroComunidade_CursoExtensaoFormSet = forms.models.inlineformset_factory(CursoExtensao, MembroComunidade_CursoExtensao, extra=1, fields=['nome', 'carga_horaria_semanal', 'entidade', 'telefone', 'email', 'cpf', 'data_nascimento', 'funcao'])
PrevisaoOrcamentaria_CursoExtensaoFormSet = forms.models.inlineformset_factory(CursoExtensao, PrevisaoOrcamentaria_CursoExtensao, extra=1, min_num=0, max_num=1, fields=['inscricoes', 'convenios', 'patrocinios', 'fonte_financiamento', 'honorarios', 'passagens', 'alimentacao', 'hospedagem', 'divulgacao', 'material_consumo', 'xerox', 'certificados', 'outros', 'outros_especificacao', 'identificacao', 'fundacao', 'outro_orgao_gestor'])
