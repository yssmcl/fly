# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-14 15:43
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('docente', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='docente',
            name='campus',
        ),
        migrations.RemoveField(
            model_name='docente',
            name='centro',
        ),
        migrations.RemoveField(
            model_name='docente',
            name='curso',
        ),
        migrations.DeleteModel(
            name='Docente',
        ),
    ]