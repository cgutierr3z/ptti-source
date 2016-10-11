#from __future__ import unicode_literals

from django.apps import AppConfig
from django.db.models.signals import post_migrate
from django.contrib.auth.models import Group, Permission
from django.contrib.auth.management import create_permissions

def add_group_permissions(apps, schema_editor):
    for app_config in apps.get_app_configs():
        create_permissions(app_config, apps=apps, verbosity=0)

    #administrador
    group, created = Group.objects.get_or_create(name='administrador')
    if created:
        change_psicologo = Permission.objects.get(codename='change_psicologo')
        add_psicologo = Permission.objects.get(codename='add_psicologo')
        group.permissions.add(change_psicologo)
        group.permissions.add(add_psicologo)

        change_estudiante = Permission.objects.get(codename='change_estudiante')
        add_estudiante = Permission.objects.get(codename='add_estudiante')
        group.permissions.add(change_estudiante)
        group.permissions.add(add_estudiante)

        change_institucion = Permission.objects.get(codename='change_institucion')
        add_institucion = Permission.objects.get(codename='add_institucion')
        group.permissions.add(change_institucion)
        group.permissions.add(add_institucion)

        change_grupo = Permission.objects.get(codename='change_grupo')
        add_grupo = Permission.objects.get(codename='add_grupo')
        group.permissions.add(change_grupo)
        group.permissions.add(add_grupo)
        group.save()

    #psicologo
    group, created = Group.objects.get_or_create(name='psicologo')
    if created:
        #group.permissions.add()
        #group.save()
        pass

    #estudiante
    group, created = Group.objects.get_or_create(name='estudiante')
    if created:
        #group.permissions.add()
        #group.save()
        pass

class PttiConfig(AppConfig):
    name = 'ptti'

    def ready(self):
        post_migrate.connect(add_group_permissions, sender=self)
