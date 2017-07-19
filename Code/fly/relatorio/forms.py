from django import forms

from .models import Relatorio, CertificadoRelatorio


class RelatorioForm(forms.ModelForm):
    class Meta:
        model = Relatorio
        fields = ['periodo_inicio', 'periodo_fim', 'publico_atingido', 'resumo', 'atividades_realizadas_programacao', 'dificuldades']

    def clean(self):
        cleaned_data = super().clean()
        
        # Validar data de início e fim.
        inicio = cleaned_data.get('periodo_inicio')
        fim = cleaned_data.get('periodo_fim')

        if inicio and fim and inicio >= fim:
            self.add_error('periodo_fim', "Data de fim deve ser após a data de início.")


class FileUploadForm(forms.Form):
    file_name = forms.CharField(max_length=200)
    file = forms.FileField()


CertificadoRelatorioFormSet = forms.models.inlineformset_factory(Relatorio, CertificadoRelatorio, extra=1, fields=['nome', 'funcao', 'frequencia', 'carga_horaria_total'])
FileUploadFormSet = forms.formset_factory(FileUploadForm, extra=1)
