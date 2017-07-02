from django.db import models
from django.contrib.auth import models as auth_models

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

class CursoExtensao(models.Model):
    user = models.ForeignKey(auth_models.User)
    
    data = models.DateTimeField()

    titulo = models.CharField(max_length=200)

    # Docente efetivo ou Agente Universitario
    coordenador = models.ForeignKey(Servidor, related_name='coordenador')
    periodo_realizacao_inicio = models.DateField()
    periodo_realizacao_fim = models.DateField()

    programa_extensao = models.ForeignKey(Programa, blank=True, null=True)

    #TODO: item 4.2 pag 31

    # Deve conter ou Unidade Administrativa ou Campus.
    unidade_administrativa = models.ForeignKey(UnidadeAdministrativa, blank=True, null=True)
    campus = models.ForeignKey(Campus, blank=True, null=True)

    centro = models.ForeignKey(Centro)
    grande_area = models.ForeignKey(GrandeArea)

    # Palavras Chave (ForeignKey)

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
    

class Servidor_CursoExtensao(models.Model):
    servidor = models.ForeignKey(Servidor)
    curso_extensao = models.ForeignKey(CursoExtensao)

    #TODO: pertence a Servidor ou Servidor_CursoExtensao?

    carga_horaria_dedicada = models.IntegerField()

    #TODO: Apenas 1 coordenador, e apenas 1 subcoordenador
    #TODO: tabela externa
    funcao = models.ForeignKey(FuncaoServidor)

class TurnoCurso(models.Model):
    # (0, 'Integral'),
    # (1, 'Noturno'),
    # (2, 'Matituno'),
    # (3, 'Tarde'),

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

class MembroComunidade_CursoExtensao(models.Model):
    curso_extensao = models.ForeignKey(CursoExtensao)

    #TODO: opcional?
    nome = models.CharField(max_length=200)
    carga_horaria_semanal = models.IntegerField()
    #TODO: instituição/entidade
    entidade = models.CharField(max_length=200)

    telefone = models.CharField(max_length=200)
    email = models.EmailField()

    #TODO: opcional?
    cpf = models.CharField(max_length=200)
    data_nascimento = models.DateField()

    funcao = models.CharField(max_length=200)

    #TODO: 19.3 plano de trabalho??
