from django.db import models

from curso_extensao.models import CursoExtensao

class Relatorio(models.Model):
    projeto_extensao = models.ForeignKey(CursoExtensao)

    periodo_inicio = models.DateField()
    periodo_fim = models.DateField()

    publico_atingido = models.CharField(max_length=200)

    # TODO: Item 9.2: Inserir onde o certificado sera gerado: PROEX ou Centro de Coordenação / Órgão Promotor
    #  orgao_gerador_certificado = models.CharField(max_length=200)

    resumo = models.CharField(max_length=200)

    atividades_realizadas_programacao = models.CharField(max_length=200)

    dificuldades = models.CharField(max_length=200)

    data = models.DateTimeField(auto_now_add=True)


class FuncaoCertificado(models.Model):
    nome = models.CharField(max_length=200)

    def __str__(self):
        return self.nome


class CertificadoRelatorio(models.Model):
    relatorio = models.ForeignKey(Relatorio)

    nome = models.CharField(max_length=200)
    # TODO: Para a função, conferir todos os tipos, pois os que já haviam sido cadastrados não possuem o tipo participante, por exemplo
    funcao = models.ForeignKey(FuncaoCertificado)
    frequencia = models.DecimalField(max_digits=10, decimal_places=2)
    carga_horaria_total = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.nome
