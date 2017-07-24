from django.db import models

from base.models import CursoUnioeste, Centro, Campus

class Docente(models.Model):
    nome_completo = models.CharField(max_length=200)
    cpf = models.CharField(max_length=200)
    email = models.EmailField()
    telefone = models.CharField(max_length=200)

    curso = models.ForeignKey(CursoUnioeste)
    centro = models.ForeignKey(Centro)
    campus = models.ForeignKey(Campus)

    pais = models.CharField(max_length=200)
    estado = models.CharField(max_length=200)
    cidade = models.CharField(max_length=200)
    logradouro = models.CharField(max_length=200)
    complemento = models.CharField(max_length=200, blank=True, null=True)
    cep = models.IntegerField()

    def __str__(self):
        return self.nome_completo

class Comissao(models.Model):
    mandato_inicio = models.DateField()
    mandato_fim = models.DateField()

    docente = models.ForeignKey(Docente)

    observacao = models.CharField(max_length=200)
