from django.conf.urls import url

from . import views

app_name = 'ptti'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^usuario/nuevo$',views.nuevo_usuario, name='nuevo_usuario'),
]
