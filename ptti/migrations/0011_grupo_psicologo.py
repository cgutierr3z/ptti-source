# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-10-09 12:49
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ptti', '0010_auto_20161009_0404'),
    ]

    operations = [
        migrations.AddField(
            model_name='grupo',
            name='psicologo',
            field=models.ForeignKey(default=27, on_delete=django.db.models.deletion.CASCADE, to='ptti.Psicologo'),
            preserve_default=False,
        ),
    ]