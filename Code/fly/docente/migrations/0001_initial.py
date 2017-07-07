# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-07 03:54
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Docente',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome_completo', models.CharField(max_length=200)),
                ('cpf', models.CharField(max_length=200)),
                ('email', models.EmailField(max_length=254)),
                ('telefone', models.CharField(max_length=200)),
                ('colegiado', models.CharField(blank=True, max_length=200, null=True)),
                ('pais', models.CharField(max_length=200)),
                ('estado', models.CharField(max_length=200)),
                ('cidade', models.CharField(max_length=200)),
                ('logradouro', models.CharField(max_length=200)),
                ('complemento', models.CharField(blank=True, max_length=200, null=True)),
                ('cep', models.IntegerField()),
                ('campus', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.Campus')),
                ('centro', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.Centro')),
                ('curso', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.CursoUnioeste')),
            ],
        ),
    ]
