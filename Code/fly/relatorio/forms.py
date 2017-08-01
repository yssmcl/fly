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

        if inicio and fim and inicio > fim:
            self.add_error('periodo_fim', "Data de início não deve ser após a data de fim.")

    resumo = forms.CharField(max_length=Relatorio._meta.get_field('resumo').max_length, widget=forms.Textarea)
    atividades_realizadas_programacao = forms.CharField(max_length=Relatorio._meta.get_field('atividades_realizadas_programacao').max_length, widget=forms.Textarea)
    dificuldades = forms.CharField(max_length=Relatorio._meta.get_field('dificuldades').max_length, widget=forms.Textarea)



class FileUploadForm(forms.Form):
    file_name = forms.CharField(max_length=200)
    file = forms.FileField()


CertificadoRelatorioFormSet = forms.models.inlineformset_factory(Relatorio, CertificadoRelatorio, extra=0, fields=['nome', 'funcao', 'frequencia', 'carga_horaria_total'])
FileUploadFormSet = forms.formset_factory(FileUploadForm, extra=0)
