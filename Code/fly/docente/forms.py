from django import forms

from base.models import Docente

class DocenteForm(forms.ModelForm):
    class Meta:
        model = Docente
        fields = [
            'nome_completo',
            'cpf',
            'email',
            'telefone',
            'curso',
            'centro',
            'campus',
            'pais',
            'estado',
            'cidade',
            'logradouro',
            'complemento',
            'cep'
        ]
