import os

def create_group(name, permissions):
    group = Group.objects.create(name=name)
    [group.permissions.add(permission) for permission in permissions]


def define_groups():
    permissionsAdmin = [
        Permission.objects.get(codename='change_psicologo'),
        Permission.objects.get(codename='add_psicologo'),
        Permission.objects.get(codename='change_estudiante'),
        Permission.objects.get(codename='add_estudiante'),
        Permission.objects.get(codename='change_institucion'),
        Permission.objects.get(codename='add_institucion'),
        Permission.objects.get(codename='change_grupo'),
        Permission.objects.get(codename='add_grupo'),
        Permission.objects.get(codename='change_testti'),
        Permission.objects.get(codename='add_testti'),
    ]
    create_group('administrador', permissionsAdmin)

    permissionsPsico = [
        Permission.objects.get(codename='asignar'),
        Permission.objects.get(codename='diagnosticar'),
    ]
    create_group('psicologo', permissionsPsico)

    permissionsEst = [

    ]
    create_group('estudiante', permissionsEst)

if __name__ == '__main__':
    print "Inicializando ptti..."
    
    import django
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ptti_source.settings')
    django.setup()
    from django.contrib.auth.models import Group, Permission

    define_groups()
