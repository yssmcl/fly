from django.db import models


class MembrosComunidade(models.Model):
    nome = models.CharField(max_length=200)

    def __str__(self):
        return self.nome


class Programa(models.Model):
    nome = models.CharField(max_length=200)

    def __str__(self):
        return self.nome


class UnidadeAdministrativa(models.Model):
    nome = models.CharField(max_length=200)

    def __str__(self):
        return self.nome


class Campus(models.Model):
    nome = models.CharField(max_length=200)

    def __str__(self):
        return self.nome


class Centro(models.Model):
    nome = models.CharField(max_length=200)

    def __str__(self):
        return self.nome


class GrandeArea(models.Model):
    nome = models.CharField(max_length=200)

    def __str__(self):
        return self.nome


class AreaTematica(models.Model):
    nome = models.CharField(max_length=200)

    def __str__(self):
        return self.nome


class LinhaExtensao(models.Model):
    nome = models.CharField(max_length=200)

    def __str__(self):
        return self.nome


class CursoUnioeste(models.Model):
    nome = models.CharField(max_length=200)

    def __str__(self):
        return self.nome


class TipoServidor(models.Model):
    nome = models.CharField(max_length=200)

    def __str__(self):
        return self.nome


class Servidor(models.Model):
    nome_completo = models.CharField(max_length=200)
    tipo = models.ForeignKey(TipoServidor)

    regime_trabalho = models.IntegerField()

    colegiado = models.CharField(max_length=200, blank=True, null=True)
    centro = models.ForeignKey(Centro)

    # Deve conter ou Unidade Administrativa ou Campus.
    unidade_administrativa = models.ForeignKey(UnidadeAdministrativa, blank=True, null=True)
    campus = models.ForeignKey(Campus, blank=True, null=True)

    email = models.EmailField()
    telefone = models.CharField(max_length=200)

    pais = models.CharField(max_length=200)
    estado = models.CharField(max_length=200)
    cidade = models.CharField(max_length=200)
    logradouro = models.CharField(max_length=200)
    complemento = models.CharField(max_length=200)
    cep = models.IntegerField()

    def __str__(self):
        return self.nome_completo


class TipoGestaoRecursosFinanceiros(models.Model):
    nome = models.CharField(max_length=200)

    def __str__(self):
        return self.nome


class FuncaoServidor(models.Model):
    nome = models.CharField(max_length=200)

    def __str__(self):
        return self.nome


class EstadoProjeto(models.Model):
    nome = models.CharField(max_length=200)

    def __str__(self):
        return self.nome

class Comissao(models.Model):
    mandato_inicio = models.DateField()
    mandato_fim = models.DateField()

    docente = models.ForeignKey(Docente)

    observacao = models.CharField(max_length=200)
