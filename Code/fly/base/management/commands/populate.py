from django.core.management.base import BaseCommand, CommandError
from base.models import *
from curso_extensao.models import *
from relatorio.models import *

class Command(BaseCommand):
    help = 'Populate the database with necessary information.'

    @staticmethod
    def saveList(class_, list_):
        print("Iniciando insercao em '{}'".format(class_.__name__))
        for nome in list_:
            if not class_.objects.filter(nome=nome).exists():
                class_(nome=nome).save()
                print("Adicionando '{} em '{}'".format(nome, class_.__name__))

    def handle(self, *args, **options):
        campus_list = [
            'Cascavel',
            'Foz do Iguaçu',
            'Francisco Beltrão',
            'Marechal Cândido Rondon',
            'Toledo',
        ]

        centro_list = [
            'CECA',
            'CCET',
            'CCBS',
            'CCSA',
            'CCMF',
            'CECE',
            'CCH',
            'CCHEL',
            'CCA',
            'CCHS',
            'CEL',
        ]

        unidade_administrativa_list = [
            'HUOP',
            'REITORIA',
        ]

        grande_area_list = [
            'Ciências Exatas e da Terra',
            'Ciências Biológicas',
            'Engenharias',
            'Ciências da Saúde',
            'Ciências Agrárias',
            'Ciências Sociais Aplicadas',
            'Ciências Humanas',
            'Linguística, Letras e Artes',
            'Outros',
        ]

        area_tematica_list = [
            'Comunicação',
            'Meio Ambiente',
            'Cultura',
            'Saúde',
            'Direitos Humanos e Justiça',
            'Tecnologia e Produção',
            'Educação',
            'Trabalho',
        ]

        linha_extensao_list = [
            'Alfabetização, leitura e escrita',
            'Artes cênicas',
            'Artes integradas',
            'Artes plásticas',
            'Artes visuais',
            'Comunicação estratégica',
            'Desenvolvimento de produtos',
            'Desenvolvimento humano',
            'Desenvolvimento regional',
            'Desenvolvimento rural e questões agrárias',
            'Desenvolvimento tecnológico',
            'Desenvolvimento urbano',
            'Direitos individuais e coletivos',
            'Divulgação científica e tecnológica',
            'Educação profissional',
            'Empreendedorismo',
            'Emprego e renda',
            'Endemias e epidemias',
            'Esporte e lazer',
            'Estilismo',
            'Fármacos e medicamentos',
            'Formação de professores',
            'Gestão do trabalho',
            'Gestão informacional',
            'Gestão institucional',
            'Gestão pública',
            'Grupos sociais vulneráveis',
            'Infância e adolescência',
            'Inovação tecnológica',
            'Jornalismo',
            'Jovens e adultos',
            'Línguas estrangeiras',
            'Metodologia e estratégias de ensino/aprendizagem',
            'Mídias',
            'Mídias-artes',
            'Música',
            'Organizações da sociedade civil e movimentos sociais populares',
            'Patrimônio cultural, histórico e natural',
            'Pessoas com deficiências, incapacidades e necessidades especiais',
            'Propriedade intelectual e patente',
            'Questões ambientais',
            'Recursos hídricos',
            'Resíduos sólidos',
            'Saúde animal',
            'Saúde da família',
            'Saúde e proteção no trabalho',
            'Saúde humana',
            'Segurança alimentar e nutricional',
            'Segurança pública e defesa social',
            'Tecnologia da informação',
            'Terceira idade',
            'Turismo',
            'Uso de drogas e dependência química',
        ]

        curso_list = [
            'Administração',
            'Ciências Contábeis',
            'Direito',
            'Hotelaria',
            'Turismo',
            'Ciência da Computação',
            'Engenharia Elétrica',
            'Engenharia Mecânica',
            'Matemática',
            'Enfermagem',
            'Letras Port./Espanhol',
            'Letras Port./Inglês',
            'Pedagogia',
        ]

        tipo_servidor_list = [
            'Docente Efetivo',
            'Docente Temporário',
            'Agente Universitário',
        ]

        tipo_gestao_recurso_financeiro_list = [
            'Unioeste',
            'PRAP',
            'Secretaria Financeira',
            'Fundação',
            'Outros',
        ]

        funcao_servidor_list = [
            'Coordenador(a)',
            'Subcoordenador(a)',
            'Supervisor(a)',
            'Colaborador(a)',
            'Autor(a)',
            'Consultor(a)',
            'Instrutor(a)',
            'Ministrante',
        ]

        turno_curso_list = [
            'Integral',
            'Noturno',
            'Matituno',
            'Tarde',
        ]

        estado_projeto_list = ['Não submetido', 'Atividade Concluída', 'Atividade em Andamento', 'Atividade com Interrupção Temporária', 'Arquivo PRPPG', 'Arquivado protocolo geral - Cancelado', 'Arquivado protocolo geral - Concluído', 'Projeto cancelado pela comissão de pesquisa', 'Projeto suspenso temporariamente', 'Atividade cancelada', 'Processo inadimplente', 'Em tramitação', 'Projeto cancelado por exoneração do coordenador', 'Projeto cancelado por aposentadoria do coordenador', 'Grupo de Pesquisa em Andamento', 'CR  com o docente - exonerado', 'Relatório final em tramitação', 'Atividade inadimplente - relatório final', 'Atividade inadimplente - relatório anual', 'Atividade não aprovada pela Comissão de Extensão', 'Atividade inadimplente']

        funcao_certificado_list = [
            'Coordenador(a)',
            'Subcoordenador(a)',
            'Supervisor(a)',
            'Colaborador(a)',
            'Autor(a)',
            'Consultor(a)',
            'Instrutor(a)',
            'Ministrante',
            'Palestrante',
            'Participante',
        ]

        self.saveList(Campus, campus_list)
        self.saveList(Centro, centro_list)
        self.saveList(UnidadeAdministrativa, unidade_administrativa_list)
        self.saveList(GrandeArea, grande_area_list)
        self.saveList(AreaTematica, area_tematica_list)
        self.saveList(LinhaExtensao, linha_extensao_list)
        self.saveList(CursoUnioeste, curso_list)
        self.saveList(TipoServidor, tipo_servidor_list)
        self.saveList(TipoGestaoRecursosFinanceiros, tipo_gestao_recurso_financeiro_list)
        self.saveList(FuncaoServidor, funcao_servidor_list)
        self.saveList(TurnoCurso, turno_curso_list)
        self.saveList(EstadoProjeto, estado_projeto_list)
        self.saveList(FuncaoCertificado, funcao_certificado_list)

        #TODO: remove
        print("Iniciando insercao em 'Servidor'")

        if not Servidor.objects.filter(nome_completo='Foo').exists():
            s = Servidor()
            s.nome_completo = 'Foo'
            s.tipo = TipoServidor.objects.all().first()
            s.regime_trabalho = 1
            s.colegiado = 'colegiado_foo'
            s.centro = Centro.objects.all().first()
            s.campus = Campus.objects.all().first()
            s.email = 'foo@foo.com'
            s.telefone = '12345678'
            s.pais = 'foo'
            s.estado = 'foo'
            s.cidade = 'foo'
            s.logradouro = 'foo'
            s.complemento = 'foo'
            s.cep = 12345678
            s.save()
            print("Adicionando Foo em Servidor")

        if not Servidor.objects.filter(nome_completo='Bar').exists():
            s = Servidor()
            s.nome_completo = 'Bar'
            s.tipo = TipoServidor.objects.all().first()
            s.regime_trabalho = 1
            s.colegiado = 'colegiado_bar'
            s.centro = Centro.objects.all().first()
            s.campus = Campus.objects.all().first()
            s.email = 'bar@bar.com'
            s.telefone = '12345678'
            s.pais = 'bar'
            s.estado = 'bar'
            s.cidade = 'bar'
            s.logradouro = 'bar'
            s.complemento = 'bar'
            s.cep = 12345678
            s.save()
            print("Adicionando Bar em Servidor")

