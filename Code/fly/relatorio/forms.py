from django import forms

from .models import Relatorio, CertificadoRelatorio


class RelatorioForm(forms.ModelForm):
    class Meta:
        model = Relatorio
        fields = ['periodo_inicio', 'periodo_fim', 'publico_atingido', 'resumo', 'atividades_realizadas_programacao', 'dificuldades']

    # comentario = forms.CharField(max_length=Parecer._meta.get_field('comentario').max_length, widget=forms.Textarea)


class FileUploadForm(forms.Form):
    file_name = forms.CharField(max_length=200)
    file = forms.FileField()


CertificadoRelatorioFormSet = forms.models.inlineformset_factory(Relatorio, CertificadoRelatorio, extra=1, fields=['nome', 'funcao', 'frequencia', 'carga_horaria_total'])
FileUploadFormSet = forms.formset_factory(FileUploadForm, extra=1)
