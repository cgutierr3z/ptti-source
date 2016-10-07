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
                    return render(request,'login_error.html')
                else:
                    auth_login(request, acceso)
                    return HttpResponseRedirect('/perfil')
            else:
                return render(request,'login_error.html',{'formulario':formulario})
    else:
        formulario = AuthenticationForm()
    return render(request,'login.html',{'formulario':formulario,'guest':guest})

@login_required(login_url='/login/')
def logout(request):
    auth_logout(request)
    return HttpResponseRedirect('/')

@login_required(login_url='/login/')
def perfil(request):
    usuario = request.user
    return  render(request,'perfil.html', {'usuario':usuario})

#vistas de usuarios

@login_required(login_url='/login/')
def usuarios(request):
    usuarios_lista = Usuario.objects.order_by('date_joined')
    context = {'usuarios_lista': usuarios_lista}
    return render(request, 'usuarios.html', context)

@login_required(login_url='/login/')
def crear_usuario(request):
    if request.method=='POST':
        formulario = FormNuevoUsuario(request.POST)
        if formulario.is_valid():
            formulario.save()
            return HttpResponseRedirect('/usuarios')
    else:
        formulario = FormNuevoUsuario()
    return render(request, 'usuario_crear.html', {'formulario':formulario})

@login_required(login_url='/login')
def editar_usuario(request, user_id):
    user = get_object_or_404(Usuario, pk=user_id)
    if request.method=='POST':
        formulario = FormEditarUsuario(request.POST, instance=user)
        if formulario.is_valid():
            formulario.save()
            return HttpResponseRedirect('/usuarios')
    else:
        formulario = FormEditarUsuario(instance=user)
    return render(request, 'usuario_editar.html', {'formulario':formulario})

@login_required(login_url='/login/')
def borrar_usuario(request, user_id):
    user = get_object_or_404(Usuario, pk=user_id)
    user.delete()
    return HttpResponseRedirect('/usuarios')

#vistas instituciones

@login_required(login_url='/login/')
def instituciones(request):
    instituciones_lista = Institucion.objects.order_by('nit')
    context = {'instituciones_lista': instituciones_lista}
    return render(request, 'instituciones.html', context)

@login_required(login_url='/login/')
def crear_institucion(request):
    if request.method == 'POST':
        formulario = FormInstitucion(request.POST)
        if formulario.is_valid():
            ins = formulario.save(commit=False)
            ins.save()
            return HttpResponseRedirect('/instituciones')
    else:
        formulario = FormInstitucion()
    return render(request, 'institucion_form.html', {'formulario':formulario})


@login_required(login_url='/login')
def editar_institucion(request, ins_id):
    ins = get_object_or_404(Institucion, pk=ins_id)
    if request.method == 'POST':
        formulario = FormInstitucion(request.POST, instance=ins)
        if formulario.is_valid():
            #ins = formulario.save(commit=False)
            formulario.save()
            return HttpResponseRedirect('/instituciones')
    else:
        formulario = FormInstitucion(instance=ins)
    return render(request, 'institucion_form.html', {'formulario':formulario})

@login_required(login_url='/login/')
def borrar_institucion(request, ins_id):
    ins = get_object_or_404(Institucion, pk=ins_id)
    ins.delete()
    return HttpResponseRedirect('/instituciones')

#vistas para grupos

@login_required(login_url='/login/')
def grupos(request):
    grupos_lista = Grupo.objects.order_by('nombre')
    context = {'grupos_lista': grupos_lista}
    return render(request, 'grupos.html', context)

@login_required(login_url='/login/')
def crear_grupo(request):
    if request.method == 'POST':
        formulario = FormGrupo(request.POST)
        if formulario.is_valid():
            gru = formulario.save(commit=False)
            gru.save()
            return HttpResponseRedirect('/grupos')
    else:
        formulario = FormGrupo()
    return render(request, 'grupo_form.html', {'formulario':formulario})


@login_required(login_url='/login')
def editar_grupo(request, gru_id):
    gru = get_object_or_404(Grupo, pk=gru_id)
    if request.method == 'POST':
        formulario = FormGrupo(request.POST, instance=gru)
        if formulario.is_valid():
            #ins = formulario.save(commit=False)
            formulario.save()
            return HttpResponseRedirect('/grupos')
    else:
        formulario = FormGrupo(instance=gru)
    return render(request, 'grupo_form.html', {'formulario':formulario})

@login_required(login_url='/login/')
def borrar_grupo(request, gru_id):
    gru = get_object_or_404(Grupo, pk=gru_id)
    gru.delete()
    return HttpResponseRedirect('/grupos')
