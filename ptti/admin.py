from django.contrib import admin

# Register your models here.

from .models import Institucion, Grupo

class InstitucionAdmin(admin.ModelAdmin):
    list_display    = ['nit','nombre','direccion','telefono','cuidad','web']
    search_fields   = ['nit','nombre','direccion','telefono','cuidad','web']

admin.site.register(Institucion, InstitucionAdmin)

class GrupoAdmin(admin.ModelAdmin):
    list_display    = ['institucion','jornada','grado','nombre']
    search_fields   = ['institucion','jornada','grado','nombre']

admin.site.register(Grupo, GrupoAdmin)

from .models import Usuario, Administrador, Psicologo, Estudiante

admin.site.register(Usuario)
admin.site.register(Administrador)
admin.site.register(Psicologo)
admin.site.register(Estudiante)
