from django.conf.urls import url

from . import views

app_name = 'ptti'
urlpatterns = [
    url(r'^$', views.login, name='index'),
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^perfil/$', views.perfil, name='perfil'),
    
    url(r'^usuarios/$',views.usuarios, name='usuarios'),
    url(r'^usuarios/crear$',views.crear_usuario, name='crear_usuario'),
    url(r'^usuarios/editar/(?P<user_id>[0-9]+)$',views.editar_usuario, name='editar_usuario'),
    url(r'^usuarios/desactivar/(?P<user_id>[0-9]+)$',views.desactivar_usuario, name='desactivar_usuario'),
    url(r'^usuarios/activar/(?P<user_id>[0-9]+)$',views.activar_usuario, name='activar_usuario'),

    url(r'^instituciones/$',views.instituciones, name='instituciones'),
    url(r'^instituciones/crear$',views.crear_institucion, name='crear_institucion'),
    url(r'^instituciones/editar/(?P<ins_id>[0-9]+)$',views.editar_institucion, name='editar_institucion'),
    url(r'^instituciones/desactivar/(?P<ins_id>[0-9]+)$',views.desactivar_institucion, name='desactivar_institucion'),
    url(r'^instituciones/activar/(?P<ins_id>[0-9]+)$',views.activar_institucion, name='activar_institucion'),

    url(r'^grupos/$',views.grupos, name='grupos'),
    url(r'^grupos/crear$',views.crear_grupo, name='crear_grupo'),
    url(r'^grupos/editar/(?P<gru_id>[0-9]+)$',views.editar_grupo, name='editar_grupo'),
    url(r'^grupos/desactivar/(?P<gru_id>[0-9]+)$',views.desactivar_grupo, name='desactivar_grupo'),
    url(r'^grupos/activar/(?P<gru_id>[0-9]+)$',views.activar_grupo, name='activar_grupo'),
]
