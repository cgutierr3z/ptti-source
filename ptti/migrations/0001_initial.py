# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-10-11 02:41
from __future__ import unicode_literals

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone

class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0008_alter_user_username_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.ASCIIUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=30, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('is_administrador', models.BooleanField(default=False, verbose_name='Administrador')),
                ('is_psicologo', models.BooleanField(default=False, verbose_name='Psicologo')),
                ('is_estudiante', models.BooleanField(default=False, verbose_name='Estudiante')),
                ('tipo_docto', models.CharField(choices=[('CEDULA CUIDADANIA', 'CEDULA CUIDADANIA'), ('CEDULA EXTRANJERIA', 'CEDULA EXTRANJERIA'), ('PASAPORTE', 'PASAPORTE'), ('TARJETA IDENTIDAD', 'TARJETA IDENTIDAD')], max_length=20, verbose_name='Tipo documento')),
                ('no_docto', models.CharField(max_length=20, verbose_name='Numero documento')),
                ('fecha_nac', models.DateField(verbose_name='Fecha nacimiento')),
                ('genero', models.CharField(choices=[('HETEROSEXUAL', 'HETEROSEXUAL'), ('HOMOSEXUAL', 'HOMOSEXUAL'), ('LESBIANA', 'LESBIANA'), ('BISEXUAL', 'BISEXUAL'), ('INDIFERENCIADO', 'INDIFERENCIADO')], max_length=20, verbose_name='Genero')),
                ('direccion', models.CharField(max_length=100, verbose_name='Direccion')),
                ('telefono', models.CharField(max_length=15, verbose_name='Telefono')),
            ],
            options={
                'db_table': 'auth_user',
                'verbose_name': 'Usuario',
                'verbose_name_plural': 'Usuarios',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Grupo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('jornada', models.CharField(choices=[('MANANA', 'MANANA'), ('TARDE', 'TARDE'), ('UNICA', 'UNICA'), ('NOCTURNA', 'NOCTURNA'), ('SABATINA', 'SABATINA')], max_length=200)),
                ('grado', models.CharField(choices=[('PRIMARIA', (('0', 'CERO'), ('1', 'PRIMERO'), ('2', 'SEGUNDO'), ('3', 'TERCERO'), ('4', 'CUARTO'), ('5', 'QUINTO'))), ('SECUNDARIA', (('6', 'SEXTO'), ('7', 'SEPTIMO'), ('8', 'OCTAVO'), ('9', 'NOVENO'), ('10', 'DECIMO'), ('11', 'UNDECIMO')))], max_length=200)),
                ('nombre', models.CharField(max_length=200)),
                ('is_active', models.BooleanField(default=True, verbose_name='Activar')),
            ],
            options={
                'verbose_name': 'Grupo',
                'verbose_name_plural': 'Grupos',
            },
        ),
        migrations.CreateModel(
            name='Institucion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nit', models.CharField(max_length=200, unique=True, verbose_name='NIT')),
                ('nombre', models.CharField(max_length=200)),
                ('direccion', models.CharField(max_length=200)),
                ('telefono', models.CharField(max_length=200)),
                ('ciudad', models.CharField(max_length=200)),
                ('web', models.URLField(verbose_name='Sitio web')),
                ('is_active', models.BooleanField(default=True, verbose_name='Activar')),
            ],
            options={
                'verbose_name': 'Institucion',
                'verbose_name_plural': 'Instituciones',
            },
        ),
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
        migrations.CreateModel(
            name='Administrador',
            fields=[
                ('usuario_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Administrador',
                'verbose_name_plural': 'Administradores',
            },
            bases=('ptti.usuario',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Estudiante',
            fields=[
                ('usuario_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Estudiante',
                'verbose_name_plural': 'Estudiantes',
            },
            bases=('ptti.usuario',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Psicologo',
            fields=[
                ('usuario_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Psicologo',
                'verbose_name_plural': 'Psicologos',
            },
            bases=('ptti.usuario',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
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
        migrations.AddField(
            model_name='grupo',
            name='institucion',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ptti.Institucion'),
        ),
        migrations.AddField(
            model_name='usuario',
            name='groups',
            field=models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups'),
        ),
        migrations.AddField(
            model_name='usuario',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions'),
        ),
        migrations.AddField(
            model_name='testasignado',
            name='estudiante',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ptti.Estudiante'),
        ),
        migrations.AddField(
            model_name='grupo',
            name='psicologo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ptti.Psicologo'),
        ),
        migrations.AddField(
            model_name='estudiante',
            name='grupo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ptti.Grupo'),
        ),
    ]
