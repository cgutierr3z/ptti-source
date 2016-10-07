# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-10-04 22:51
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ptti', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PreguntaTestTI',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pregunta', models.CharField(max_length=200)),
                ('numero', models.IntegerField(unique=True)),
            ],
            options={
                'verbose_name': 'Pregunta Test TI',
                'verbose_name_plural': 'Preguntas Test TI',
            },
        ),
        migrations.CreateModel(
            name='RespuestaEstudiante',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pregunta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ptti.PreguntaTestTI')),
            ],
            options={
                'verbose_name': 'Test Asignado',
                'verbose_name_plural': 'Tests Asignados',
            },
        ),
        migrations.CreateModel(
            name='RespuestaTestTI',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('respuesta', models.CharField(max_length=200)),
                ('pregunta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ptti.PreguntaTestTI')),
            ],
            options={
                'verbose_name': 'Respuesta Test TI',
                'verbose_name_plural': 'Respuestas Test TI',
            },
        ),
        migrations.CreateModel(
            name='TestAsignado',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'verbose_name': 'Test Asignado',
                'verbose_name_plural': 'Tests Asignados',
            },
        ),
        migrations.CreateModel(
            name='TestTI',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=200)),
            ],
            options={
                'verbose_name': 'Test TI',
                'verbose_name_plural': 'Tests TI',
            },
        ),
        migrations.AlterModelOptions(
            name='grupo',
            options={'verbose_name': 'Grupo', 'verbose_name_plural': 'Grupos'},
        ),
        migrations.AlterModelOptions(
            name='institucion',
            options={'verbose_name': 'Institucion', 'verbose_name_plural': 'Instituciones'},
        ),
        migrations.AlterModelOptions(
            name='usuario',
            options={'verbose_name': 'Usuario', 'verbose_name_plural': 'Usuarios'},
        ),
        migrations.RemoveField(
            model_name='administrador',
            name='active',
        ),
        migrations.RemoveField(
            model_name='estudiante',
            name='active',
        ),
        migrations.RemoveField(
            model_name='psicologo',
            name='active',
        ),
        migrations.AddField(
            model_name='testasignado',
            name='estudiante',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ptti.Estudiante'),
        ),
        migrations.AddField(
            model_name='testasignado',
            name='test',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ptti.TestTI'),
        ),
        migrations.AddField(
            model_name='respuestaestudiante',
            name='respuesta',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ptti.RespuestaTestTI'),
        ),
        migrations.AddField(
            model_name='respuestaestudiante',
            name='test',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ptti.TestAsignado'),
        ),
        migrations.AddField(
            model_name='preguntatestti',
            name='test',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ptti.TestTI'),
        ),
    ]