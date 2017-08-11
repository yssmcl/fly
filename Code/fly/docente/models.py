from django.db import models

from base.models import CursoUnioeste, Centro, Campus

class TipoDocente(models.Model):
    nome = models.CharField(max_length=200)

    def __str__(self):
        return self.nome


class Docente(models.Model):
    nome_completo = models.CharField(max_length=200)
    cpf = models.CharField(max_length=200)
    email = models.EmailField()
    telefone = models.CharField(max_length=200)

    curso = models.ForeignKey(CursoUnioeste)
    colegiado = models.CharField(max_length=200)
    centro = models.ForeignKey(Centro)
    campus = models.ForeignKey(Campus)

    pais = models.CharField(max_length=200)
    estado = models.CharField(max_length=200)
    cidade = models.CharField(max_length=200)
    logradouro = models.CharField(max_length=200)
    complemento = models.CharField(max_length=200, blank=True, null=True)
    cep = models.IntegerField()

    tipo_docente = models.ForeignKey(TipoDocente)

    def __str__(self):
        return self.nome_completo
