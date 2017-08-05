import os

from django.db import models
from django.dispatch import receiver

from curso_extensao.models import CursoExtensao


class EstadoRelatorio(models.Model):
    nome = models.CharField(max_length=200)

    def __str__(self):
        return self.nome


class Relatorio(models.Model):
    projeto_extensao = models.ForeignKey(CursoExtensao)

    periodo_inicio = models.DateField()
    periodo_fim = models.DateField()

    publico_atingido = models.IntegerField()

    # TODO: Item 9.2: Inserir onde o certificado sera gerado: PROEX ou Centro de Coordenação / Órgão Promotor
    #  orgao_gerador_certificado = models.CharField(max_length=200)

    resumo = models.CharField(max_length=200)

    atividades_realizadas_programacao = models.CharField(max_length=200)

    dificuldades = models.CharField(max_length=200)

    data = models.DateTimeField(auto_now_add=True)

    estado = models.ForeignKey(EstadoRelatorio)


class FuncaoCertificado(models.Model):
    nome = models.CharField(max_length=200)

    def __str__(self):
        return self.nome


class RelatorioFile(models.Model):
    relatorio = models.ForeignKey(Relatorio)
    nome = models.CharField(max_length=200)
    file = models.FileField(upload_to='uploads/')


@receiver(models.signals.post_delete, sender=RelatorioFile)
def auto_delete_file(sender, instance, **kwargs):
    if instance.file and os.path.isfile(instance.file.path):
        os.remove(instance.file.path)


class CertificadoRelatorio(models.Model):
    relatorio = models.ForeignKey(Relatorio)

    nome = models.CharField(max_length=200)
    # TODO: Para a função, conferir todos os tipos, pois os que já haviam sido cadastrados não possuem o tipo participante, por exemplo
    funcao = models.ForeignKey(FuncaoCertificado)
    frequencia = models.DecimalField(max_digits=10, decimal_places=2)
    carga_horaria_total = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.nome
