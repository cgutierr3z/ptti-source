from django.contrib import admin

# Register your models here.

from .models import *

class InstitucionAdmin(admin.ModelAdmin):
    list_display    = ['nit','nombre','direccion','telefono','cuidad','web']
    search_fields   = ['nit','nombre','direccion','telefono','cuidad','web']

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

admin.site.register(Usuario,UsuariosAdmin)

class AdministradorAdmin(admin.ModelAdmin):
    raw_id_fields = ('user',)
    #fields = ('user','user_username')
    list_display    = ['username','first_name','last_name','no_docto','email','is_active']
    search_fields   = ['username','first_name','last_name','no_docto','email']

    def username(self, obj):
        return obj.user.username

    def first_name(self, obj):
        return obj.user.first_name

    def last_name(self, obj):
        return obj.user.last_name

    def no_docto(self, obj):
        return obj.user.no_docto

    def email(self, obj):
        return obj.user.email

    def is_active(self, obj):
        return obj.user.is_active

admin.site.register(Administrador,AdministradorAdmin)

class PsicologoAdmin(admin.ModelAdmin):
    raw_id_fields = ('user',)
    #fields = ('user','user_username')
    list_display    = ['username','first_name','last_name','no_docto','email','is_active']
    search_fields   = ['username','first_name','last_name','no_docto','email']

    def username(self, obj):
        return obj.user.username

    def first_name(self, obj):
        return obj.user.first_name

    def last_name(self, obj):
        return obj.user.last_name

    def no_docto(self, obj):
        return obj.user.no_docto

    def email(self, obj):
        return obj.user.email

    def is_active(self, obj):
        return obj.user.is_active

admin.site.register(Psicologo,PsicologoAdmin)

class EstudianteAdmin(admin.ModelAdmin):
    raw_id_fields = ('user','grupo')
    #fields = ('user','user_username')
    list_display    = ['username','first_name','last_name','no_docto','email','is_active']
    search_fields   = ['username','first_name','last_name','no_docto','email']

    def username(self, obj):
        return obj.user.username

    def first_name(self, obj):
        return obj.user.first_name

    def last_name(self, obj):
        return obj.user.last_name

    def no_docto(self, obj):
        return obj.user.no_docto

    def email(self, obj):
        return obj.user.email

    def is_active(self, obj):
        return obj.user.is_active

admin.site.register(Estudiante,EstudianteAdmin)
