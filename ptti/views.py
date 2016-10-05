from django.shortcuts import render

# Create your views here.
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404, render
from django.template import RequestContext
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from django.contrib.auth import login as auth_login, authenticate, logout as auth_logout
from django.contrib.auth.decorators import login_required
from .forms import *
from .models import *

def index(request):
    guest = request.user.is_anonymous()
    context = {'guest': guest}
    return render(request, 'index.html', context)

#@login_required(login_url='/login')
def nuevo_usuario(request):
    if request.method=='POST':
        formulario = FormNuevoUsuario(request.POST)
        if formulario.is_valid():
            formulario.save()
            return HttpResponseRedirect('/')
    else:
        formulario = FormNuevoUsuario()
    #return render_to_response('nuevousuario.html',{'formulario':formulario})
    return render(request, 'nuevo_usuario.html', {'formulario':formulario})

@login_required(login_url='/login')
def editar_perfil(request, user_id):
    user = get_object_or_404(Usuario, pk=user_id)
    if request.method=='POST':
        formulario = FormEditarUsuario(request.POST, instance=user)
        if formulario.is_valid():
            formulario.save()
            return HttpResponseRedirect('/usuarios')
    else:
        formulario = FormEditarUsuario(instance=user)
    return render(request, 'editar_perfil.html', {'formulario':formulario})

@login_required(login_url='/login/')
def usuarios(request):
    usuarios_lista = Usuario.objects.order_by('date_joined')
    context = {'usuarios_lista': usuarios_lista}
    return render(request, 'usuarios.html', context)

def login(request):
    guest = request.user.is_anonymous()
    if not guest:
        return HttpResponseRedirect('/perfil')
    if request.method == 'POST':
        formulario = AuthenticationForm(request.POST)
        if formulario.is_valid:
            usuario = request.POST['username']
            clave = request.POST['password']
            acceso = authenticate(username=usuario, password=clave)
            if acceso is not None:
                if not acceso.is_active:
                    return render(request,'inactivo.html')
                else:
                    auth_login(request, acceso)
                    return HttpResponseRedirect('/perfil')
            else:
                return render(request,'error_usuario.html',{'formulario':formulario})
    else:
        formulario = AuthenticationForm()
    return render(request,'ingresar.html',{'formulario':formulario,'guest':guest})

@login_required(login_url='/login/')
def logout(request):
    auth_logout(request)
    return HttpResponseRedirect('/')

@login_required(login_url='/login/')
def perfil(request):

    usuario = request.user
    return  render(request,'perfil.html', {'usuario':usuario})
