from django.db import models

from curso_extensao.models import CursoExtensao

class Relatorio(models.Model):
    projeto_extensao = models.ForeignKey(CursoExtensao)

    periodo_realizacao_inicio = models.DateField()
    periodo_realizacao_fim = models.DateField()

    colegiado = models.CharField(max_length=200)

    publico_atingido = models.CharField(max_length=200)
