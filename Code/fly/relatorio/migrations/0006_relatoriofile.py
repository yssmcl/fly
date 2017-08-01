# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-01 13:41
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('relatorio', '0005_auto_20170723_2049'),
    ]

    operations = [
        migrations.CreateModel(
            name='RelatorioFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='uploads/')),
                ('relatorio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='relatorio.Relatorio')),
            ],
        ),
    ]