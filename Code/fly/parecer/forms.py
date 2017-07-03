from django import forms
from django.utils.translation import ugettext_lazy as _

from .models import Parecer

class ParecerForm(forms.ModelForm):
    class Meta:
        model = Parecer
        fields = ['estado_parecer', 'comentario']

    comentario = forms.CharField(max_length=Parecer._meta.get_field('comentario').max_length, widget=forms.Textarea)
