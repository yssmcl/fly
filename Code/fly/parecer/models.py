from django.db import models

from curso_extensao.models import CursoExtensao
from base.models import EstadoProjeto

class Parecer(models.Model):
    projeto_extensao = models.ForeignKey(CursoExtensao) #TODO: herança

    estado_parecer = models.ForeignKey(EstadoProjeto)

    comentario = models.CharField(max_length=200)
