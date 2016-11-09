from django.contrib import admin

# Register your models here.

from .models import *

class InstitucionAdmin(admin.ModelAdmin):
    list_display    = ['nit','nombre','direccion','telefono','ciudad','web']
    search_fields   = ['nit','nombre','direccion','telefono','ciudad','web']

admin.site.register(Institucion, InstitucionAdmin)

class GrupoAdmin(admin.ModelAdmin):
    raw_id_fields   = ('institucion',)
    list_display    = ['institucion','jornada','grado','nombre']
    search_fields   = ['institucion','jornada','grado','nombre']

admin.site.register(Grupo, GrupoAdmin)

class UsuariosAdmin(admin.ModelAdmin):
    fields          = ['email','first_name','last_name','tipo_docto','no_docto','fecha_nac','genero','direccion','telefono','password','is_administrador','is_psicologo','is_estudiante','is_staff','is_active','is_superuser']
    list_display    = ['username','email','first_name','last_name','tipo_docto','no_docto','fecha_nac','genero','direccion','telefono','is_administrador','is_psicologo','is_estudiante','is_staff','is_active','is_superuser']
    search_fields   = ['email','first_name','last_name','tipo_docto','no_docto','fecha_nac','genero','direccion','telefono']

    actions = ['desactivar']

    def desactivar(self, request, queryset):
        rows_updated = queryset.update(is_active='False')
        if rows_updated == 1:
            message_bit = "1 story was"
        else:
            message_bit = "%s stories were" % rows_updated
        self.message_user(request, "%s successfully marked as published." % message_bit)
    desactivar.short_description = "Desactivar cuentas selecionadas"

admin.site.register(Usuario)

admin.site.register(Administrador)

admin.site.register(Psicologo)

admin.site.register(Estudiante)

admin.site.register(TestTI)

admin.site.register(PreguntaTestTI)

admin.site.register(RespuestaTestTI)

admin.site.register(TestAsignado)

admin.site.register(RespuestaEstudiante)
