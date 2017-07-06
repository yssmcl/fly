from django import forms
from django.utils.translation import ugettext_lazy as _

from .models import Relatorio, CertificadoRelatorio

class RelatorioForm(forms.ModelForm):
    class Meta:
        model = Relatorio
        fields = ['periodo_inicio', 'periodo_fim', 'publico_atingido', 'resumo', 'atividades_realizadas_programacao', 'dificuldades']

    # comentario = forms.CharField(max_length=Parecer._meta.get_field('comentario').max_length, widget=forms.Textarea)


CertificadoRelatorioFormSet = forms.models.inlineformset_factory(Relatorio, CertificadoRelatorio, extra=1, fields=['nome', 'funcao', 'frequencia', 'carga_horaria_total'])

