from django import forms
from django.utils.translation import ugettext_lazy as _

from .models import CursoExtensao, Servidor, Servidor_CursoExtensao, PalavraChave_CursoExtensao, Discente_CursoExtensao, MembroComunidade_CursoExtensao, PrevisaoOrcamentaria_CursoExtensao

class CursoExtensaoForm(forms.ModelForm):
    class Meta:
        model = CursoExtensao
        fields = ['titulo', 'coordenador', 'periodo_realizacao_inicio', 'periodo_realizacao_fim', 'programa_extensao', 'unidade_administrativa', 'campus', 'centro', 'grande_area', 'area_tematica_principal', 'area_tematica_secundaria', 'linha_extensao', 'publico_alvo', 'numero_pessoas_beneficiadas', 'carga_horaria_total', 'numero_vagas', 'local_inscricao', 'resumo', 'programacao']

    coordenador = forms.ModelChoiceField(queryset=Servidor.objects.exclude(tipo__nome='Docente Temporário'))
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

        # Validar data de início e fim.
        inicio = cleaned_data.get('periodo_realizacao_inicio')
        fim = cleaned_data.get('periodo_realizacao_fim')

        if inicio and fim and inicio >= fim:
            self.add_error('periodo_realizacao_fim', "Data de fim deve ser após a data de início.")

        # Validar que coordenador não seja Docente Temporário.
        coordenador = cleaned_data.get('coordenador')

        if coordenador and coordenador.tipo.nome == 'Docente Temporário':
            self.add_error('coordenador', "Coordenador não pode ser docente temporário.")

        # Validar que as áreas temáticas são diferentes.
        area1 = cleaned_data.get('area_tematica_principal')
        area2 = cleaned_data.get('area_tematica_secundaria')

        if area1 and area2 and area1 == area2:
            self.add_error('area_tematica_secundaria', "Áreas temáticas devem ser diferentes.")

        return cleaned_data


class PrevisaoOrcamentaria_CursoExtensaoForm(forms.ModelForm):
    class Meta:
        model = PrevisaoOrcamentaria_CursoExtensao
        fields = ['inscricoes', 'convenios', 'patrocinios', 'fonte_financiamento', 'honorarios', 'passagens', 'alimentacao', 'hospedagem', 'divulgacao', 'material_consumo', 'xerox', 'certificados', 'outros', 'outros_especificacao', 'identificacao', 'fundacao', 'outro_orgao_gestor']

    def clean(self):
        cleaned_data = super(PrevisaoOrcamentaria_CursoExtensaoForm, self).clean()
        
        # Validar especificação de campo `outros`.
        outros = cleaned_data.get('outros')
        outros_especificacao = cleaned_data.get('outros_especificacao')

        if outros and not outros_especificacao:
            self.add_error('outros_especificacao', _("This field is required."))

        # Validar gestor de recursos.
        identificacao = cleaned_data.get('identificacao')
        fundacao = cleaned_data.get('fundacao')
        outro_orgao_gestor = cleaned_data.get('outro_orgao_gestor')

        if identificacao:
            if identificacao.nome == 'Fundação':
                if not fundacao:
                    self.add_error('fundacao', _("This field is required."))
            elif identificacao.nome == 'Outros':
                if not outro_orgao_gestor:
                    self.add_error('outro_orgao_gestor', _("This field is required."))

        return cleaned_data


Servidor_CursoExtensaoFormSet = forms.models.inlineformset_factory(CursoExtensao, Servidor_CursoExtensao, extra=1, fields=['servidor', 'carga_horaria_dedicada', 'funcao'])
Discente_CursoExtensaoFormSet = forms.models.inlineformset_factory(CursoExtensao, Discente_CursoExtensao, extra=1, fields=['nome', 'curso', 'serie', 'turno', 'carga_horaria_semanal', 'telefone', 'email'])
PalavraChave_CursoExtensaoFormSet = forms.models.inlineformset_factory(CursoExtensao, PalavraChave_CursoExtensao, extra=3, min_num=1, max_num=3, fields=['nome'])
MembroComunidade_CursoExtensaoFormSet = forms.models.inlineformset_factory(CursoExtensao, MembroComunidade_CursoExtensao, extra=1, fields=['nome', 'carga_horaria_semanal', 'entidade', 'telefone', 'email', 'cpf', 'data_nascimento', 'funcao'])
PrevisaoOrcamentaria_CursoExtensaoFormSet = forms.models.inlineformset_factory(CursoExtensao, PrevisaoOrcamentaria_CursoExtensao, extra=1, min_num=0, max_num=1, form=PrevisaoOrcamentaria_CursoExtensaoForm)
