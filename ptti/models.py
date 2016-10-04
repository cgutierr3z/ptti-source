from __future__ import unicode_literals

from django.db import models

# Create your models here.

from django.contrib.auth.models import AbstractUser

#modelo de instiuciones
class Institucion(models.Model):
    nit         = models.CharField(max_length=200,unique=True)
    nombre      = models.CharField(max_length=200)
    direccion   = models.CharField(max_length=200)
    telefono    = models.CharField(max_length=200)
    cuidad      = models.CharField(max_length=200)
    web         = models.URLField(max_length=200)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = "Institucion"
        verbose_name_plural = "Instituciones"

#modelo de grupos
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

    class Meta:
        verbose_name = "Grupo"
        verbose_name_plural = "Grupos"

#modelo de usuarios
class Usuario(AbstractUser):
    no_docto    = models.CharField(max_length=64)

    class Meta:
        db_table = 'auth_user'
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"

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
