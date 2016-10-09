from django.conf.urls import url

from . import views

app_name = 'ptti'
urlpatterns = [
    url(r'^$', views.login, name='index'),
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^password-reset/$', views.reset_password, name='reset_password'),
    url(r'^password-reset/confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$',views.reset_password_confirm, name='reset_password_confirm'),

    url(r'^perfil/$', views.perfil, name='perfil'),
    url(r'^perfil/editar/(?P<user_id>[0-9]+)$',views.perfil_editar, name='perfil_editar'),
    url(r'^perfil/contrasena/(?P<user_id>[0-9]+)$', views.perfil_cambiar_contrasena, name='perfil_cambiar_contrasena'),

    url(r'^usuarios/$',views.usuarios, name='usuarios'),
    url(r'^usuarios/crear$',views.crear_usuario, name='crear_usuario'),
    url(r'^usuarios/editar/(?P<user_id>[0-9]+)$',views.editar_usuario, name='editar_usuario'),
    url(r'^usuarios/activar/(?P<user_id>[0-9]+)$',views.activar_usuario, name='activar_usuario'),
    url(r'^usuarios/desactivar/(?P<user_id>[0-9]+)$',views.desactivar_usuario, name='desactivar_usuario'),

    url(r'^administradores/$',views.administradores, name='administradores'),
    url(r'^administradores/crear$',views.crear_administrador, name='crear_administrador'),
    url(r'^administradores/editar/(?P<user_id>[0-9]+)$',views.editar_administrador, name='editar_administrador'),
    url(r'^administradores/activar/(?P<user_id>[0-9]+)$',views.activar_administrador, name='activar_administrador'),
    url(r'^administradores/desactivar/(?P<user_id>[0-9]+)$',views.desactivar_administrador, name='desactivar_administrador'),

    url(r'^psicologos/$',views.psicologos, name='psicologos'),
    url(r'^psicologos/crear$',views.crear_psicologo, name='crear_psicologo'),
    url(r'^psicologos/editar/(?P<user_id>[0-9]+)$',views.editar_psicologo, name='editar_psicologo'),
    url(r'^psicologos/activar/(?P<user_id>[0-9]+)$',views.activar_psicologo, name='activar_psicologo'),
    url(r'^psicologos/desactivar/(?P<user_id>[0-9]+)$',views.desactivar_psicologo, name='desactivar_psicologo'),

    url(r'^estudiantes/$',views.estudiantes, name='estudiantes'),
    url(r'^estudiantes/crear$',views.crear_estudiante, name='crear_estudiante'),
    url(r'^estudiantes/editar/(?P<user_id>[0-9]+)$',views.editar_estudiante, name='editar_estudiante'),
    url(r'^estudiantes/activar/(?P<user_id>[0-9]+)$',views.activar_estudiante, name='activar_estudiante'),
    url(r'^estudiantes/desactivar/(?P<user_id>[0-9]+)$',views.desactivar_estudiante, name='desactivar_estudiante'),

    url(r'^instituciones/$',views.instituciones, name='instituciones'),
    url(r'^instituciones/crear$',views.crear_institucion, name='crear_institucion'),
    url(r'^instituciones/editar/(?P<ins_id>[0-9]+)$',views.editar_institucion, name='editar_institucion'),
    url(r'^instituciones/activar/(?P<ins_id>[0-9]+)$',views.activar_institucion, name='activar_institucion'),
    url(r'^instituciones/desactivar/(?P<ins_id>[0-9]+)$',views.desactivar_institucion, name='desactivar_institucion'),

    url(r'^grupos/$',views.grupos, name='grupos'),
    url(r'^grupos/crear$',views.crear_grupo, name='crear_grupo'),
    url(r'^grupos/editar/(?P<gru_id>[0-9]+)$',views.editar_grupo, name='editar_grupo'),
    url(r'^grupos/activar/(?P<gru_id>[0-9]+)$',views.activar_grupo, name='activar_grupo'),
    url(r'^grupos/desactivar/(?P<gru_id>[0-9]+)$',views.desactivar_grupo, name='desactivar_grupo'),

]
