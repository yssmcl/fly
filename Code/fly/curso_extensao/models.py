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

class Servidor(models.Model):
    TIPOS = (
        (0, 'Docente Efetivo'),
        (1, 'Docente Temporário'),
        (2, 'Agente Universitário')
    )

    nome_completo = models.CharField(max_length=200)
    tipo = models.IntegerField(choices=TIPOS)

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
    complemento = models.IntegerField()
    cep = models.IntegerField()

    def __str__(self):
        return self.nome_completo

class PrevisaoOrcamentaria(models.Model):
    # Receitas.
    inscricoes = models.DecimalField(max_digits=10, decimal_places=2)
    convenios = models.DecimalField(max_digits=10, decimal_places=2)
    patrocinios = models.DecimalField(max_digits=10, decimal_places=2)

    #TODO: tipo dos campos??
    fonte_financiamento = models.DecimalField(max_digits=10, decimal_places=2)

    # Despesas.
    honorarios = models.DecimalField(max_digits=10, decimal_places=2)
    passagens = models.DecimalField(max_digits=10, decimal_places=2)
    alimentacao = models.DecimalField(max_digits=10, decimal_places=2)
    hospedagem = models.DecimalField(max_digits=10, decimal_places=2)
    divulgacao = models.DecimalField(max_digits=10, decimal_places=2)
    material_de_consumo = models.DecimalField(max_digits=10, decimal_places=2)
    xerox = models.DecimalField(max_digits=10, decimal_places=2)
    certificados = models.DecimalField(max_digits=10, decimal_places=2)
    
    outros = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    outros_especificacao = models.CharField(max_length=200, blank=True, null=True)

class GestaoRecursosFinanceiros(models.Model):
    IDENTIFICACOES = (
        (0, 'Unioeste'),
        (1, 'PRAP'),
        (2, 'Secretaria Financeira'),
        (3, 'Fundação'),
        (4, 'Outros')
    )

    identificacao = models.IntegerField(choices=IDENTIFICACOES)

    fundacao = models.CharField(max_length=200, blank=True, null=True)
    outros = models.CharField(max_length=200, blank=True, null=True)

class CursoExtensao(models.Model):
    user = models.ForeignKey(auth_models.User)
    
    data = models.DateTimeField()

    titulo = models.CharField(max_length=200)

    # Docente efetivo ou Agente Universitario
    coordenador = models.ForeignKey(Servidor, related_name='coordenador')
    periodo_de_realizacao = models.CharField(max_length=200)

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

    #21 é opcional caso #20 seja Null
    previsao_orcamentaria = models.ForeignKey(PrevisaoOrcamentaria, blank=True, null=True)


class PalavraChave_CursoExtensao(models.Model):
    curso_extensao = models.ForeignKey(CursoExtensao)
    valor = models.CharField(max_length=200)

class Servidor_CursoExtensao(models.Model):
    FUNCOES = (
        (0, 'Coordenador(a)'),
        (1, 'Subcoordenador(a)'),
        (2, 'Supervisor(a)'),
        (3, 'Colaborador(a)'),
        (4, 'Autor(a)'),
        (5, 'Consultor(a)'),
        (6, 'Instrutor(a)'),
        (7, 'Ministrante(a)')
    )

    servidor = models.ForeignKey(Servidor)
    curso_extensao = models.ForeignKey(CursoExtensao)

    #TODO: pertence a Servidor ou Servidor_CursoExtensao?

    carga_horaria_dedicada = models.IntegerField()

    #TODO: Apenas 1 coordenador, e apenas 1 subcoordenador
    #TODO: tabela externa
    funcao = models.IntegerField(choices=FUNCOES)

class Discente_CursoExtensao(models.Model):
    #TODO: cadastrar discente? (manyToMany)

    TURNOS = (
        (0, 'Integral'),
        (1, 'Noturno'),
        (2, 'Matituno'),
        (3, 'Tarde'),
    )

    curso_extensao = models.ForeignKey(CursoExtensao)

    #TODO: buscar do CSV
    nome = models.CharField(max_length=200)
    curso = models.ForeignKey(CursoUnioeste)

    serie = models.IntegerField()
    turno = models.IntegerField(choices=TURNOS)

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
