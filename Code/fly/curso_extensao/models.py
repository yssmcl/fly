from django.db import models
from django.contrib.auth import models as auth_models

from base.models import Servidor, Programa, UnidadeAdministrativa, Campus, Centro, GrandeArea, AreaTematica, LinhaExtensao, TipoGestaoRecursosFinanceiros, FuncaoServidor, CursoUnioeste, EstadosProjeto

class CursoExtensao(models.Model):
    user = models.ForeignKey(auth_models.User)
    
    data = models.DateTimeField()

    titulo = models.CharField(max_length=200)

    estado = models.ForeignKey(EstadosProjeto)

    # Docente efetivo ou Agente Universitario
    coordenador = models.ForeignKey(Servidor, related_name='coordenador')
    periodo_realizacao_inicio = models.DateField()
    periodo_realizacao_fim = models.DateField()

    programa_extensao = models.ForeignKey(Programa, blank=True, null=True)

    # Deve conter ou Unidade Administrativa ou Campus.
    unidade_administrativa = models.ForeignKey(UnidadeAdministrativa, blank=True, null=True)
    campus = models.ForeignKey(Campus, blank=True, null=True)

    centro = models.ForeignKey(Centro)
    grande_area = models.ForeignKey(GrandeArea)

    area_tematica_principal = models.ForeignKey(AreaTematica, related_name='area_tematica_principal')
    area_tematica_secundaria = models.ForeignKey(AreaTematica, related_name='area_tematica_secundaria', blank=True, null=True)

    linha_extensao = models.ForeignKey(LinhaExtensao)

    publico_alvo = models.CharField(max_length=200)

    numero_pessoas_beneficiadas = models.IntegerField()

    carga_horaria_total = models.IntegerField()
    numero_vagas = models.IntegerField()

    local_inscricao = models.CharField(max_length=200)

    resumo = models.CharField(max_length=200)

    programacao = models.CharField(max_length=200)

    servidores = models.ManyToManyField(Servidor, related_name='servidores', through='Servidor_CursoExtensao')

    def __str__(self):
        return self.titulo


class PrevisaoOrcamentaria_CursoExtensao(models.Model):
    curso_extensao = models.OneToOneField(CursoExtensao)

    # Receitas.
    inscricoes = models.DecimalField(max_digits=10, decimal_places=2)
    convenios = models.DecimalField(max_digits=10, decimal_places=2)
    patrocinios = models.DecimalField(max_digits=10, decimal_places=2)

    fonte_financiamento = models.DecimalField(max_digits=10, decimal_places=2)

    # Despesas.
    honorarios = models.DecimalField(max_digits=10, decimal_places=2)
    passagens = models.DecimalField(max_digits=10, decimal_places=2)
    alimentacao = models.DecimalField(max_digits=10, decimal_places=2)
    hospedagem = models.DecimalField(max_digits=10, decimal_places=2)
    divulgacao = models.DecimalField(max_digits=10, decimal_places=2)
    material_consumo = models.DecimalField(max_digits=10, decimal_places=2)
    xerox = models.DecimalField(max_digits=10, decimal_places=2)
    certificados = models.DecimalField(max_digits=10, decimal_places=2)
    
    #TODO: validar:
    outros = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    outros_especificacao = models.CharField(max_length=200, blank=True, null=True)

    # Gestao dos recursos financeiros
    #TODO: validar:
    identificacao = models.ForeignKey(TipoGestaoRecursosFinanceiros)
    fundacao = models.CharField(max_length=200, blank=True, null=True)
    outro_orgao_gestor = models.CharField(max_length=200, blank=True, null=True)


class PalavraChave_CursoExtensao(models.Model):
    curso_extensao = models.ForeignKey(CursoExtensao)
    nome = models.CharField(max_length=200)


class Servidor_CursoExtensao(models.Model):
    servidor = models.ForeignKey(Servidor)
    curso_extensao = models.ForeignKey(CursoExtensao)

    carga_horaria_dedicada = models.IntegerField()

    funcao = models.ForeignKey(FuncaoServidor)

    plano_trabalho = models.CharField(max_length=200)


class TurnoCurso(models.Model):
    nome = models.CharField(max_length=200)

    def __str__(self):
        return self.nome
    

class Discente_CursoExtensao(models.Model):
    curso_extensao = models.ForeignKey(CursoExtensao)

    #TODO: buscar do CSV
    nome = models.CharField(max_length=200)
    curso = models.ForeignKey(CursoUnioeste)

    serie = models.IntegerField()
    turno = models.ForeignKey(TurnoCurso)

    carga_horaria_semanal = models.IntegerField()

    telefone = models.CharField(max_length=200)
    email = models.EmailField()

    plano_trabalho = models.CharField(max_length=200)


class MembroComunidade_CursoExtensao(models.Model):
    curso_extensao = models.ForeignKey(CursoExtensao)

    nome = models.CharField(max_length=200)
    carga_horaria_semanal = models.IntegerField()
    #TODO: instituição/entidade
    entidade = models.CharField(max_length=200)

    telefone = models.CharField(max_length=200)
    email = models.EmailField()

    cpf = models.CharField(max_length=200)
    data_nascimento = models.DateField()

    funcao = models.CharField(max_length=200)

    plano_trabalho = models.CharField(max_length=200)
