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
    # (0, 'Docente Efetivo'),
    # (1, 'Docente Temporário'),
    # (2, 'Agente Universitário')
    
    nome = models.CharField(max_length=200)

    def __str__(self):
        return self.nome

class Servidor(models.Model):
    nome_completo = models.CharField(max_length=200)
    tipo = models.ForeignKey(TipoServidor)

    regime_trabalho = models.IntegerField()

    #TODO: que tipo de campo é esse??
    #TODO: é um curso :D
    #TODO: pode ser nulo
    colegiado = models.CharField(max_length=200)
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
    # (0, 'Unioeste'),
    # (1, 'PRAP'),
    # (2, 'Secretaria Financeira'),
    # (3, 'Fundação'),
    # (4, 'Outros')

    nome = models.CharField(max_length=200)

    def __str__(self):
        return self.nome


class FuncaoServidor(models.Model):
    # (0, 'Coordenador(a)'),
    # (1, 'Subcoordenador(a)'),
    # (2, 'Supervisor(a)'),
    # (3, 'Colaborador(a)'),
    # (4, 'Autor(a)'),
    # (5, 'Consultor(a)'),
    # (6, 'Instrutor(a)'),
    # (7, 'Ministrante(a)')

    nome = models.CharField(max_length=200)

    def __str__(self):
        return self.nome
    