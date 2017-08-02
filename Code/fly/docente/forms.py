from django import forms

from .models import Docente

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
            'colegiado',
            'campus',
            'pais',
            'estado',
            'cidade',
            'logradouro',
            'complemento',
            'cep',
            'tipo_docente',
        ]
