# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-07-03 17:13
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0003_auto_20170702_1302'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='EstadosProjeto',
            new_name='EstadoProjeto',
        ),
    ]