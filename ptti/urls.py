from django.conf.urls import url

from . import views

app_name = 'ptti'
urlpatterns = [
    url(r'^$', views.login, name='index'),
    url(r'^usuarios/$',views.usuarios, name='usuarios'),
    url(r'^usuarios/nuevo$',views.nuevo_usuario, name='nuevo_usuario'),
    url(r'^usuarios/editar/(?P<user_id>[0-9]+)$',views.editar_perfil, name='editar_perfil'),
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^perfil/$', views.perfil, name='perfil'),

]
