from __future__ import unicode_literals

from django.db import models

# Create your models here.

from django.contrib.auth.models import AbstractUser
import datetime

#modelo de instiuciones
class Institucion(models.Model):
    class Meta:
        verbose_name = "Institucion"
        verbose_name_plural = "Instituciones"

    nit         = models.CharField(max_length=200,unique=True)
    nombre      = models.CharField(max_length=200)
    direccion   = models.CharField(max_length=200)
    telefono    = models.CharField(max_length=200)
    ciudad      = models.CharField(max_length=200)
    web         = models.URLField(max_length=200)

    def __str__(self):
        return self.nombre

#modelo de grupos
class Grupo(models.Model):
    class Meta:
        verbose_name = "Grupo"
        verbose_name_plural = "Grupos"

    JORNADA_LIST = [
        ('M', 'MANANA'),
        ('T', 'TARDE'),
        ('U', 'UNICA'),
        ('N', 'NOCTURNA'),
        ('S', 'SABATINA'),
    ]
    GRADOS_LIST = [
        ('PRIMARIA',(
                ('0','CERO'),
                ('1','PRIMERO'),
                ('2','SEGUNDO'),
                ('3','TERCERO'),
                ('4','CUARTO'),
                ('5','QUINTO'),
            )
        ),
        ('SECUNDARIA',(
                ('6','SEXTO'),
                ('7','SEPTIMO'),
                ('8','OCTAVO'),
                ('9','NOVENO'),
                ('10','DECIMO'),
                ('11','UNDECIMO'),
            )
        ),
    ]
    institucion = models.ForeignKey(Institucion, on_delete=models.CASCADE)
    jornada     = models.CharField(max_length=200,choices=JORNADA_LIST)
    grado       = models.CharField(max_length=200,choices=GRADOS_LIST)
    nombre      = models.CharField(max_length=200)


    def __str__(self):
        return self.nombre + "-" + self.institucion.nombre


#modelo de usuarios
class Usuario(AbstractUser):
    class Meta:
        db_table = 'auth_user'
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"

    TIPO_DOC_LIST = [
        ('CC', 'CEDULA CUIDADANIA'),
        ('CE', 'CEDULA EXTRANJERIA'),
        ('PAS', 'PASAPORTE'),
        ('TI', 'TARJETA IDENTIDAD'),
    ]
    GENERO_LIST= [
        ('HT', 'HETEROSEXUAL'),
        ('HM', 'HOMOSEXUAL'),
        ('LE', 'LESBIANA'),
        ('BI', 'BISEXUAL'),
        ('IN', 'INDIFERENCIADO'),
    ]

    is_administrador    = models.BooleanField('Administrador',default=False)
    is_psicologo        = models.BooleanField('Psicologo',default=False)
    is_estudiante       = models.BooleanField('Estudiante',default=False)
    tipo_docto          = models.CharField('Tipo documento',max_length=20,choices=TIPO_DOC_LIST)
    no_docto            = models.CharField('Numero documento',max_length=20)
    fecha_nac           = models.DateField('Fecha nacimiento',default='31/12/1999')
    genero              = models.CharField('Genero',max_length=20,choices=GENERO_LIST)
    direccion           = models.CharField('Direccion',max_length=100)
    telefono            = models.CharField('Telefono',max_length=15)

    def administrador(self):
        return self.is_administrador

    def psicologo(self):
        return self.is_psicologo

    def estudiante(self):
        return self.is_estudiante



class Administrador(models.Model):
    class Meta:
        verbose_name = "Administrador"
        verbose_name_plural = "Administradores"

    user        = models.OneToOneField(Usuario, on_delete=models.CASCADE)
    #active      = models.BooleanField(default=True)

class Psicologo(models.Model):
    class Meta:
        verbose_name = "Psicologo"
        verbose_name_plural = "Psicologos"

    user        = models.OneToOneField(Usuario, on_delete=models.CASCADE)
    #active      = models.BooleanField(default=True)

class Estudiante(models.Model):
    class Meta:
        verbose_name = "Estudiante"
        verbose_name_plural = "Estudiantes"

    user        = models.OneToOneField(Usuario, on_delete=models.CASCADE)
    #active      = models.BooleanField(default=True)
    grupo       = models.ForeignKey(Grupo, on_delete=models.CASCADE)

#modelo de Test
class TestTI(models.Model):
    nombre      = models.CharField(max_length=200)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = "Test TI"
        verbose_name_plural = "Tests TI"

class PreguntaTestTI(models.Model):
    test        = models.ForeignKey(TestTI, on_delete=models.CASCADE)
    pregunta    = models.CharField(max_length=200)
    numero      = models.IntegerField(unique=True)

    def __str__(self):
        return self.numero + " " +  self.pregunta

    class Meta:
        verbose_name = "Pregunta Test TI"
        verbose_name_plural = "Preguntas Test TI"

class RespuestaTestTI(models.Model):
    pregunta    = models.ForeignKey(PreguntaTestTI, on_delete=models.CASCADE)
    respuesta   = models.CharField(max_length=200)

    def __str__(self):
        return self.respuesta

    class Meta:
        verbose_name = "Respuesta Test TI"
        verbose_name_plural = "Respuestas Test TI"

#modelo de respuestas a los test
class TestAsignado(models.Model):
    estudiante  = models.ForeignKey(Estudiante, on_delete=models.CASCADE)
    test        = models.ForeignKey(TestTI, on_delete=models.CASCADE)

    def __str__(self):
        return self.test + " " + self.estudiante

    class Meta:
        verbose_name = "Test Asignado"
        verbose_name_plural = "Tests Asignados"

class RespuestaEstudiante(models.Model):
    test        = models.ForeignKey(TestAsignado, on_delete=models.CASCADE)
    pregunta    = models.ForeignKey(PreguntaTestTI, on_delete=models.CASCADE)
    respuesta   = models.ForeignKey(RespuestaTestTI, on_delete=models.CASCADE)

    def __str__(self):
        return self.test + " " + self.estudiante

    class Meta:
        verbose_name = "Test Asignado"
        verbose_name_plural = "Tests Asignados"
