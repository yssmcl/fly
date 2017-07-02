# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-07-02 15:25
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('base', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CursoExtensao',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.DateTimeField()),
                ('titulo', models.CharField(max_length=200)),
                ('periodo_realizacao_inicio', models.DateField()),
                ('periodo_realizacao_fim', models.DateField()),
                ('publico_alvo', models.CharField(max_length=200)),
                ('numero_pessoas_beneficiadas', models.IntegerField()),
                ('carga_horaria_total', models.IntegerField()),
                ('numero_vagas', models.IntegerField()),
                ('local_inscricao', models.CharField(max_length=200)),
                ('resumo', models.CharField(max_length=200)),
                ('programacao', models.CharField(max_length=200)),
                ('area_tematica_principal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='area_tematica_principal', to='base.AreaTematica')),
                ('area_tematica_secundaria', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='area_tematica_secundaria', to='base.AreaTematica')),
                ('campus', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='base.Campus')),
                ('centro', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.Centro')),
                ('coordenador', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='coordenador', to='base.Servidor')),
                ('grande_area', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.GrandeArea')),
                ('linha_extensao', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.LinhaExtensao')),
                ('programa_extensao', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='base.Programa')),
            ],
        ),
        migrations.CreateModel(
            name='Discente_CursoExtensao',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=200)),
                ('serie', models.IntegerField()),
                ('carga_horaria_semanal', models.IntegerField()),
                ('telefone', models.CharField(max_length=200)),
                ('email', models.EmailField(max_length=254)),
                ('plano_trabalho', models.CharField(max_length=200)),
                ('curso', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.CursoUnioeste')),
                ('curso_extensao', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='curso_extensao.CursoExtensao')),
            ],
        ),
        migrations.CreateModel(
            name='MembroComunidade_CursoExtensao',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=200)),
                ('carga_horaria_semanal', models.IntegerField()),
                ('entidade', models.CharField(max_length=200)),
                ('telefone', models.CharField(max_length=200)),
                ('email', models.EmailField(max_length=254)),
                ('cpf', models.CharField(max_length=200)),
                ('data_nascimento', models.DateField()),
                ('funcao', models.CharField(max_length=200)),
                ('plano_trabalho', models.CharField(max_length=200)),
                ('curso_extensao', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='curso_extensao.CursoExtensao')),
            ],
        ),
        migrations.CreateModel(
            name='PalavraChave_CursoExtensao',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=200)),
                ('curso_extensao', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='curso_extensao.CursoExtensao')),
            ],
        ),
        migrations.CreateModel(
            name='PrevisaoOrcamentaria_CursoExtensao',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('inscricoes', models.DecimalField(decimal_places=2, max_digits=10)),
                ('convenios', models.DecimalField(decimal_places=2, max_digits=10)),
                ('patrocinios', models.DecimalField(decimal_places=2, max_digits=10)),
                ('fonte_financiamento', models.DecimalField(decimal_places=2, max_digits=10)),
                ('honorarios', models.DecimalField(decimal_places=2, max_digits=10)),
                ('passagens', models.DecimalField(decimal_places=2, max_digits=10)),
                ('alimentacao', models.DecimalField(decimal_places=2, max_digits=10)),
                ('hospedagem', models.DecimalField(decimal_places=2, max_digits=10)),
                ('divulgacao', models.DecimalField(decimal_places=2, max_digits=10)),
                ('material_consumo', models.DecimalField(decimal_places=2, max_digits=10)),
                ('xerox', models.DecimalField(decimal_places=2, max_digits=10)),
                ('certificados', models.DecimalField(decimal_places=2, max_digits=10)),
                ('outros', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('outros_especificacao', models.CharField(blank=True, max_length=200, null=True)),
                ('fundacao', models.CharField(blank=True, max_length=200, null=True)),
                ('outro_orgao_gestor', models.CharField(blank=True, max_length=200, null=True)),
                ('curso_extensao', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='curso_extensao.CursoExtensao')),
                ('identificacao', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.TipoGestaoRecursosFinanceiros')),
            ],
        ),
        migrations.CreateModel(
            name='Servidor_CursoExtensao',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('carga_horaria_dedicada', models.IntegerField()),
                ('curso_extensao', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='curso_extensao.CursoExtensao')),
                ('funcao', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.FuncaoServidor')),
                ('servidor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.Servidor')),
            ],
        ),
        migrations.CreateModel(
            name='TurnoCurso',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=200)),
            ],
        ),
        migrations.AddField(
            model_name='discente_cursoextensao',
            name='turno',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='curso_extensao.TurnoCurso'),
        ),
        migrations.AddField(
            model_name='cursoextensao',
            name='servidores',
            field=models.ManyToManyField(related_name='servidores', through='curso_extensao.Servidor_CursoExtensao', to='base.Servidor'),
        ),
        migrations.AddField(
            model_name='cursoextensao',
            name='unidade_administrativa',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='base.UnidadeAdministrativa'),
        ),
        migrations.AddField(
            model_name='cursoextensao',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
