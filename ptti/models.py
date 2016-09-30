from __future__ import unicode_literals

from django.db import models

# Create your models here.

from django.contrib.auth.models import AbstractUser

#instiuciones
class Institucion(models.Model):
    nit         = models.CharField(max_length=200,unique=True)
    nombre      = models.CharField(max_length=200)
    direccion   = models.CharField(max_length=200)
    telefono    = models.CharField(max_length=200)
    cuidad      = models.CharField(max_length=200)
    web         = models.URLField(max_length=200)

    def __str__(self):
        return self.nombre

class Grupo(models.Model):
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

#usuarios
class Usuario(AbstractUser):
    no_docto    = models.CharField(max_length=64)
    class Meta:
        db_table = 'auth_user'

class Administrador(models.Model):
    user        = models.OneToOneField(Usuario, on_delete=models.CASCADE)
    #active      = models.BooleanField(default=True)

class Psicologo(models.Model):
    user        = models.OneToOneField(Usuario, on_delete=models.CASCADE)
    #active      = models.BooleanField(default=True)

class Estudiante(models.Model):
    user        = models.OneToOneField(Usuario, on_delete=models.CASCADE)
    #active      = models.BooleanField(default=True)
    institucion = models.ForeignKey(Institucion, on_delete=models.CASCADE)
    grupo       = models.ForeignKey(Grupo, on_delete=models.CASCADE)

class TestTI(models.Model):
    nombre      = models.CharField(max_length=200)

class PreguntasTestTI(models.Model):
    test        = models.ForeignKey(TestTI, on_delete=models.CASCADE)
    pregunta    = models.CharField(max_length=200)
    numero      = models.IntegerField(unique=True)

class RespuestasTestTI(models.Model):
    pregunta    = models.ForeignKey(PreguntasTestTI, on_delete=models.CASCADE)
    respuesta   = models.CharField(max_length=200)

class TestAsignado(models.Model):
    estudiante  = models.ForeignKey(Estudiante, on_delete=models.CASCADE)
    test        = models.ForeignKey(TestTI, on_delete=models.CASCADE)
