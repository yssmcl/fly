from django.db import models

# Create your models here.
class Pessoa(models.Model):
    nome = models.CharField(max_length=200)

class MembrosComunidade(models.Models):
    pass

class Programa(models.Model):
    pass

class UnidadeAdministrativa(models.Model):
    pass

class Campus(models.Model):
    pass

class Centro(models.Model):
    pass

class GrandeArea(models.Model):
    pass

class AreaTematica(models.Model):
    pass

class LinhaExtensao(models.Model):
    pass

class CursoExtensao(models.Model):
    data = models.DateTimeField()

    titulo = models.CharField(max_length=200)
    coordenador = models.ForeignKey(Pessoa)
    periodo_de_realizacao = models.CharField(max_length=200)

    programa_extensao = models.NullForeignKey(Programa)

    #TODO: item 4.2 pag 31

    # Deve conter ou Unidade Administrativa ou Campus
    unidade_administrativa = models.NullForeignKey(UnidadeAdministrativa)
    campus = models.NullForeignKey(Campus)

    centro = models.ForeignKey(Centro)
    grande_area = models.ForeignKey(GrandeArea)

    area_tematica_principal = models.ForeignKey(AreaTematica)
    area_tematica_secundaria = models.NullForeignKey(AreaTematica)

    linha_extensao = models.ForeignKey(LinhaExtensao)

    publico_alvo = models.CharField(max_length=200)

    numero_pessoas_beneficiadas = models.IntegerField()

    carga_horaria_total = models.IntegerField()
    numero_vagas = models.IntegerField()

    local_inscricao = models.CharField(max_length=200)

    #21 é opcional caso #20 seja Null


class PalavraChave_CursoExtensao(models.Model):
    curso_extensao = models.ForeignKey(CursoExtensao)
    valor = models.CharField(max_length=200)

