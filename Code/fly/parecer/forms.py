from django import forms
from django.utils.translation import ugettext_lazy as _

from .models import Parecer
from base.models import EstadoProjeto

class ParecerForm(forms.ModelForm):
    class Meta:
        model = Parecer
        fields = ['estado_parecer', 'numero_ata']

    estado_parecer = forms.ModelChoiceField(queryset=EstadoProjeto.objects.exclude(nome='Não submetido').exclude(nome='Submetido'))
