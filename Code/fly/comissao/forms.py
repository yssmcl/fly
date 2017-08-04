from django import forms

from .models import Comissao, Comissao_Docente

class ComissaoForm(forms.ModelForm):
    class Meta:
        model = Comissao
        fields = ['inicio', 'fim']


Comissao_DocenteFormSet = forms.models.inlineformset_factory(Comissao, Comissao_Docente, extra=0, min_num=1, fields=['docente'])
