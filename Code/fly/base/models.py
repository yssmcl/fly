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
