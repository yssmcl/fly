from django.db import models

from docente.models import Docente

class Comissao(models.Model):
    inicio = models.DateField()
    fim = models.DateField()

    membros = models.ManyToManyField(Docente, related_name='membros', through='Comissao_Docente')

class Comissao_Docente(models.Model):
    comissao = models.ForeignKey(Comissao)
    docente = models.ForeignKey(Docente)
