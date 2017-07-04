from django.db import models

from curso_extensao.models import CursoExtensao

class Relatorio(models.Model):
    projeto_extensao = models.ForeignKey(CursoExtensao)

    periodo_inicio = models.DateField()
    periodo_fim = models.DateField()

    colegiado = models.CharField(max_length=200)

    publico_atingido = models.CharField(max_length=200)

    # Inserir onde o certificado sera gerado: PROEX ou Centro de Coordenação / Órgão Promotor

    resumo = models.CharField(max_length=200)

    atividades_realizadas_programacao = models.CharField(max_length=200)

    dificuldades = models.CharField(max_length=200)

    local = models.CharField(max_length=200)

    data = models.DateField()



class Certificado(models.Model):
	nome = models.CharField(max_length=200)
	#Para a função, conferir todos os tipos, pois os que já haviam sido cadastrados não possui o tipo participante, por exemplo
	funcao = models.CharField(max_length=200)
	frequencia = models.DecimalField(max_digits=10, decimal_places=2)
	carga_horaria_total = models.DecimalField(max_digits=10, decimal_places=2)