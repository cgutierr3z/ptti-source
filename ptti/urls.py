from django.conf.urls import url

from . import views

app_name = 'ptti'
urlpatterns = [
    url(r'^$', views.login, name='index'),
    url(r'^usuarios/$',views.usuarios, name='usuarios'),
    url(r'^usuarios/crear$',views.crear_usuario, name='crear_usuario'),
    url(r'^usuarios/editar/(?P<user_id>[0-9]+)$',views.editar_usuario, name='editar_usuario'),
    url(r'^usuarios/borrar/(?P<user_id>[0-9]+)$',views.borrar_usuario, name='borrar_usuario'),
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^perfil/$', views.perfil, name='perfil'),

]
