# -*- coding: utf-8 -*-

from base.models import *
from curso_extensao.models import *
from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
from relatorio.models import *

class Command(BaseCommand):
    help = 'Populate the database with necessary information.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--cursoextensao',
            action='store_true',
            dest='cursoextensao',
            default=False,
            help='Popula curso de extensão',
        )

        parser.add_argument(
            '--relatorio',
            action='store_true',
            dest='relatorio',
            default=False,
            help='Popula relatório',
        )

    def handle(self, *args, **options):
        if options['cursoextensao']:
            self.popular_cursoextensao()
        elif options['relatorio']:
            self.popular_relatorio()
        else:
            self.save_lists()

    @staticmethod
    def saveList(class_, list_):
        print("Iniciando insercao em '{}'".format(class_.__name__))
        for nome in list_:
            if not class_.objects.filter(nome=nome).exists():
                class_(nome=nome).save()
                print("Adicionando '{} em '{}'".format(nome, class_.__name__))

    def save_lists(self):
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

            estado_relatorio_list = [
                'Não submetido',
                'Submetido',
                'Aprovado',
                'Não aprovado',
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
            self.saveList(EstadoRelatorio, estado_relatorio_list)


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

    def popular_cursoextensao(self):
        print("Iniciando insercao em 'CursoExtensao'")
        if not CursoExtensao.objects.filter(titulo='título curso 1').exists():
            c = CursoExtensao()
            c.user = auth_models.User.objects.all().first()
            c.data = timezone.now()
            c.titulo = 'título curso 1'
            c.estado = EstadoProjeto.objects.all().first()
            c.coordenador = Servidor.objects.all().first()
            c.periodo_realizacao_inicio = timezone.now()
            c.periodo_realizacao_fim = timezone.now()
            c.programa_extensao = None
            c.unidade_administrativa = UnidadeAdministrativa.objects.all().first()
            c.campus = Campus.objects.all().first()
            c.centro = Centro.objects.all().first()
            c.grande_area = GrandeArea.objects.all().first()
            c.area_tematica_principal = AreaTematica.objects.all().first()
            c.area_tematica_secundaria = AreaTematica.objects.all().last()
            c.linha_extensao = LinhaExtensao.objects.all().first()
            c.publico_alvo = 'público alvo curso 1'
            c.numero_pessoas_beneficiadas = 50
            c.carga_horaria_total = 12
            c.numero_vagas = 80
            c.local_inscricao = 'local de inscrição curso 1'
            c.resumo = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Quisque id mi et enim iaculis finibus. Maecenas posuere dolor ac lacus venenatis efficitur. In vestibulum rutrum nulla.'
            c.programacao = 'Aliquam erat volutpat. Sed et aliquet risus. Sed mattis eget felis nec placerat. Mauris imperdiet turpis sit amet lorem dictum, non fringilla tellus condimentum.'
            #  c.servidores =
            c.save()
            print("Adicionando 'título curso 1' em 'CursoExtensao'")

            print("Iniciando insercao em 'PrevisaoOrcamentaria_CursoExtensao'")
            p = PrevisaoOrcamentaria_CursoExtensao()
            p.curso_extensao = CursoExtensao.objects.all().first()
            p.inscricoes = 200
            p.convenios = 100
            p.patrocinios = 150
            p.fonte_financiamento = 190
            p.honorarios = 180
            p.passagens = 130
            p.alimentacao = 120
            p.hospedagem = 160
            p.divulgacao = 170
            p.material_consumo = 110
            p.xerox = 80
            p.certificados = 50
            p.outros = 40
            p.outros_especificacao = 'especificação outros curso 1'
            p.identificacao = TipoGestaoRecursosFinanceiros.objects.all().first()
            p.fundacao = 'fundação curso 1'
            p.outro_orgao_gestor = 'outro órgao gestor curso 1'
            p.save()
            print("Adicionando 'previsão curso 1' em 'PrevisaoOrcamentaria_CursoExtensao'")

            print("Iniciando insercao em 'PalavraChave_CursoExtensao'")
            pal1 = PalavraChave_CursoExtensao()
            pal1.curso_extensao = CursoExtensao.objects.all().first()
            pal1.nome = 'palavra-chave 1 curso 1'
            pal1.save()
            print("Adicionando 'palavra-chave 1 curso 1' em 'PalavraChave_CursoExtensao'")
            pal2 = PalavraChave_CursoExtensao()
            pal2.curso_extensao = CursoExtensao.objects.all().first()
            pal2.nome = 'palavra-chave 2 curso 1'
            pal2.save()
            print("Adicionando 'palavra-chave 2 curso 1' em 'PalavraChave_CursoExtensao'")
            pal3 = PalavraChave_CursoExtensao()
            pal3.curso_extensao = CursoExtensao.objects.all().first()
            pal3.nome = 'palavra-chave 3 curso 1'
            pal3.save()
            print("Adicionando 'palavra-chave 3 curso 1' em 'PalavraChave_CursoExtensao'")

            print("Iniciando insercao em 'Servidor_CursoExtensao'")
            sc1 = Servidor_CursoExtensao()
            sc1.curso_extensao = CursoExtensao.objects.all().first()
            sc1.servidor = Servidor.objects.all().first()
            sc1.carga_horaria_dedicada = 4
            sc1.funcao = FuncaoServidor.objects.all().first()
            sc1.plano_trabalho = 'Quisque a augue vel libero placerat vestibulum. In vitae nunc bibendum ante porttitor bibendum a eu risus. Duis lorem tortor, tempus et ipsum tincidunt, dignissim aliquam metus.'
            sc1.save()
            print("Adicionando 'Foo' em 'Servidor_CursoExtensao'")
            sc2 = Servidor_CursoExtensao()
            sc2.curso_extensao = CursoExtensao.objects.all().first()
            sc2.servidor = Servidor.objects.all().last()
            sc2.carga_horaria_dedicada = 4
            sc2.funcao = FuncaoServidor.objects.all().first()
            sc2.plano_trabalho = 'Quisque a augue vel libero placerat vestibulum. In vitae nunc bibendum ante porttitor bibendum a eu risus. Duis lorem tortor, tempus et ipsum tincidunt, dignissim aliquam metus.'
            sc2.save()
            print("Adicionando 'Bar' em 'Servidor_CursoExtensao'")

            print("Iniciando insercao em 'Discente_CursoExtensao'")
            dc1 = Discente_CursoExtensao()
            dc1.curso_extensao = CursoExtensao.objects.all().first()
            dc1.nome = 'nome discente 1 curso 1'
            dc1.curso = CursoUnioeste.objects.all().first()
            dc1.serie = 2
            dc1.turno = TurnoCurso.objects.all().first()
            dc1.carga_horaria_semanal = 20
            dc1.telefone = '35755153'
            dc1.email = 'emaildiscente1@email.com'
            dc1.plano_trabalho = 'Phasellus dictum scelerisque egestas. Nulla pharetra ligula consequat tortor varius malesuada id vitae risus. Phasellus aliquet, mauris vel tempor lacinia, felis neque feugiat nibh.'
            dc1.save()
            print("Adicionando 'discente 1 curso 1' em 'Discente_CursoExtensao'")
            dc2 = Discente_CursoExtensao()
            dc2.curso_extensao = CursoExtensao.objects.all().first()
            dc2.nome = 'nome discente 2 curso 1'
            dc2.curso = CursoUnioeste.objects.all().last()
            dc2.serie = 4
            dc2.turno = TurnoCurso.objects.all().last()
            dc2.carga_horaria_semanal = 30
            dc2.telefone = '35715453'
            dc2.email = 'emaildiscente2@email.com'
            dc2.plano_trabalho = 'Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos. Proin sit amet cursus diam, nec pulvinar augue. Ut commodo sem vitae dolor ultricies, eu volutpat.'
            dc2.save()
            print("Adicionando 'discente 2 curso 1' em 'Discente_CursoExtensao'")

            print("Iniciando insercao em 'MembroComunidade_CursoExtensao'")
            mc1 = MembroComunidade_CursoExtensao()
            mc1.curso_extensao = CursoExtensao.objects.all().first()
            mc1.nome = 'membro 1 curso 1'
            mc1.carga_horaria_semanal = 25
            mc1.entidade = 'entidade 1'
            mc1.telefone = '35845645'
            mc1.email = 'emailmembro1@email.com'
            mc1.cpf = '054.456.489-51'
            mc1.data_nascimento = timezone.now()
            mc1.funcao = 'função 1'
            mc1.plano_trabalho = 'Vestibulum bibendum enim sed nibh suscipit, ac viverra turpis volutpat. Curabitur ullamcorper sem eget molestie tempor. Suspendisse quis pellentesque sem. Fusce sagittis et leo ac cras amet.'
            mc1.save()
            print("Adicionando 'membro 1 curso 1' em 'Discente_CursoExtensao'")
            mc2 = MembroComunidade_CursoExtensao()
            mc2.curso_extensao = CursoExtensao.objects.all().first()
            mc2.nome = 'membro 2 curso 1'
            mc2.carga_horaria_semanal = 25
            mc2.entidade = 'entidade 2'
            mc2.telefone = '35465456'
            mc2.email = 'emailmembro1@email.com'
            mc2.cpf = '055.461.492-49'
            mc2.data_nascimento = timezone.now()
            mc2.funcao = 'função 2'
            mc2.plano_trabalho = 'Morbi nisl risus, dictum sed quam nec, convallis varius nisl. Aliquam vestibulum dapibus aliquet. Aliquam dignissim mi eget sodales facilisis. Aenean molestie dui eget justo tincidunt metus.'
            mc2.save()
            print("Adicionando 'membro 2 curso 1' em 'Discente_CursoExtensao'")

    def popular_relatorio(self):
        print("Iniciando insercao em 'Relatorio'")
        r = Relatorio()
        r.projeto_extensao = CursoExtensao.objects.all().first()
        r.periodo_inicio = timezone.now()
        r.periodo_fim = timezone.now()
        r.publico_atingido = 'público atingido'
        r.resumo = 'Quisque fermentum erat quis mattis ultrices. Phasellus lobortis ligula et tincidunt auctor. Proin eget eros nisi. Sed est tellus, finibus ac condimentum nec, tincidunt a orci. Sed ac nullam.'
        r.atividades_realizadas_programacao = 'Sed pulvinar felis vitae massa dapibus laoreet. Fusce vitae facilisis nibh, nec dictum purus. Interdum et malesuada fames ac ante ipsum primis in faucibus. Morbi ac lorem et orci massa nunc.'
        r.dificuldades = 'Morbi vehicula elit et molestie hendrerit. Pellentesque in lacus fermentum, egestas sapien nec, ornare urna. Nulla vitae eros efficitur, pharetra tortor nec, ullamcorper libero orci aliquam.'
        r.estado = EstadoRelatorio.objects.all().first()
        r.save()
        print("Adicionando 'relatório curso 1' em 'Relatorio'")

        print("Iniciando insercao em 'CertificadoRelatorio'")
        cr1 = CertificadoRelatorio()
        cr1.relatorio = Relatorio.objects.all().first()
        cr1.nome = 'nome 1'
        cr1.funcao = FuncaoCertificado.objects.all().first()
        cr1.frequencia = 90
        cr1.carga_horaria_total = 16
        cr1.save()
        print("Adicionando 'nome 1' em 'CertificadoRelatorio'")
        cr2 = CertificadoRelatorio()
        cr2.relatorio = Relatorio.objects.all().first()
        cr2.nome = 'nome 2'
        cr2.funcao = FuncaoCertificado.objects.all().first()
        cr2.frequencia = 70
        cr2.carga_horaria_total = 16
        cr2.save()
        print("Adicionando 'nome 2' em 'CertificadoRelatorio'")

