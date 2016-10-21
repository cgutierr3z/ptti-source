from django.shortcuts import render

# Create your views here.
#from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
#from django.template import RequestContext
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm, PasswordResetForm, PasswordChangeForm, PasswordResetForm
from django.contrib.auth import login as auth_login, authenticate, logout as auth_logout
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.views import password_reset, password_reset_confirm
from django.core.urlresolvers import reverse

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
            email = request.POST['username']
            clave = request.POST['password']

            usuario = Usuario.objects.filter(email=email)
            if len(usuario) == 1:
                usuario = Usuario.objects.filter(email=email)
                acceso = authenticate(username=usuario[0].username, password=clave)
            else:
                acceso = authenticate(username=None, password=clave)

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
    return render(request,'login.html',{'formulario':formulario})

def reset_password(request):
    return password_reset(request, template_name='password_reset_form.html',
        email_template_name='password_reset_email.html',
        subject_template_name='password_reset_subject.txt',
        post_reset_redirect=reverse('ptti:login'))

def reset_password_confirm(request, uidb64=None, token=None):
    return password_reset_confirm(request, template_name='password_reset_confirm.html',
        uidb64=uidb64, token=token, post_reset_redirect=reverse('ptti:login'))

@login_required(login_url='/login/')
def logout(request):
    auth_logout(request)
    return HttpResponseRedirect('/')


#vista de perfil

@login_required(login_url='/login/')
def perfil(request):
    usuario = request.user
    return  render(request,'perfil.html', {'usuario':usuario})


@login_required(login_url='/login')
def perfil_editar(request, user_id):
    user = get_object_or_404(Usuario, pk=user_id)
    if request.method=='POST':
        formulario = FormEditarPerfil(request.POST, instance=user)
        if formulario.is_valid():
            formulario.save()
            return HttpResponseRedirect('/perfil')
    else:
        formulario = FormEditarPerfil(instance=user)
    return render(request, 'perfil_editar.html', {'formulario':formulario,'usuario':user})

@login_required(login_url='/login')
def perfil_cambiar_contrasena(request, user_id):
    user = get_object_or_404(Usuario, pk=user_id)
    formulario = PasswordChangeForm(user)
    if request.method=='POST':
        formulario = PasswordChangeForm(user, request.POST)
        if formulario.is_valid():
            formulario.save()
            update_session_auth_hash(request, formulario.user)
            return HttpResponseRedirect('/perfil')

    return render(request, 'perfil_cambiar_contrasena.html', {'formulario':formulario})

#vistas de usuarios

@login_required(login_url='/login/')
@permission_required('ptti.change_usuario', login_url="/login/")
def usuarios(request):
    usuarios_lista = Usuario.objects.order_by('-date_joined').exclude(id=request.user.id)
    context = {'usuarios_lista': usuarios_lista}
    return render(request, 'usuarios.html', context)

@login_required(login_url='/login/')
@permission_required('ptti.add_usuario', login_url="/login/")
def crear_usuario(request):
    if request.method=='POST':
        formulario = FormCrearUsuario(request.POST)
        if formulario.is_valid():
            formulario.save()
            return HttpResponseRedirect('/usuarios')
    else:
        formulario = FormCrearUsuario()
    return render(request, 'usuario_crear.html', {'formulario':formulario})

@login_required(login_url='/login')
@permission_required('ptti.change_usuario', login_url="/login/")
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
@permission_required('ptti.change_usuario', login_url="/login/")
def desactivar_usuario(request, user_id):
    user = get_object_or_404(Usuario, pk=user_id)
    user.desactivar()
    user.save()
    return HttpResponseRedirect('/usuarios')

@login_required(login_url='/login/')
@permission_required('ptti.change_usuario', login_url="/login/")
def activar_usuario(request, user_id):
    user = get_object_or_404(Usuario, pk=user_id)
    user.activar()
    user.save()
    return HttpResponseRedirect('/usuarios')

#vistas para administrador

@login_required(login_url='/login/')
@permission_required('ptti.change_administrador', login_url="/login/")
def administradores(request):
    usuarios_lista = Administrador.objects.order_by('-date_joined').exclude(id=request.user.id)
    context = {'usuarios_lista': usuarios_lista}
    return render(request, 'usuarios.html', context)

@login_required(login_url='/login/')
@permission_required('ptti.add_administrador', login_url="/login/")
def crear_administrador(request):
    if request.method=='POST':
        formulario = FormCrearAdministrador(request.POST)
        if formulario.is_valid():
            formulario.save()
            return HttpResponseRedirect('/administradores')
    else:
        formulario = FormCrearAdministrador()
    return render(request, 'usuario_crear.html', {'formulario':formulario})

@login_required(login_url='/login')
@permission_required('ptti.change_administrador', login_url="/login/")
def editar_administrador(request, user_id):
    user = get_object_or_404(Usuario, pk=user_id)
    if request.method=='POST':
        formulario = FormEditarAdministrador(request.POST, instance=user)
        if formulario.is_valid():
            formulario.save()
            return HttpResponseRedirect('/administradores')
    else:
        formulario = FormEditarAdministrador(instance=user)
    return render(request, 'usuario_editar.html', {'formulario':formulario})

@login_required(login_url='/login/')
@permission_required('ptti.change_administrador', login_url="/login/")
def desactivar_administrador(request, user_id):
    user = get_object_or_404(Administrador, pk=user_id)
    user.desactivar()
    user.save()
    return HttpResponseRedirect('/administradores')

@login_required(login_url='/login/')
@permission_required('ptti.change_administrador', login_url="/login/")
def activar_administrador(request, user_id):
    user = get_object_or_404(Administrador, pk=user_id)
    user.activar()
    user.save()
    return HttpResponseRedirect('/administradores')

#vistas para Psicologo

@login_required(login_url='/login/')
@permission_required('ptti.change_psicologo', login_url="/login/")
def psicologos(request):
    usuarios_lista = Psicologo.objects.order_by('-date_joined').exclude(id=request.user.id)
    context = {'usuarios_lista': usuarios_lista}
    return render(request, 'usuarios.html', context)

@login_required(login_url='/login/')
@permission_required('ptti.add_psicologo', login_url="/login/")
def crear_psicologo(request):
    if request.method=='POST':
        formulario = FormCrearPsicologo(request.POST)
        if formulario.is_valid():
            formulario.save()
            return HttpResponseRedirect('/psicologos')
    else:
        formulario = FormCrearPsicologo()
    return render(request, 'usuario_crear.html', {'formulario':formulario})

@login_required(login_url='/login')
@permission_required('ptti.change_psicologo', login_url="/login/")
def editar_psicologo(request, user_id):
    user = get_object_or_404(Usuario, pk=user_id)
    if request.method=='POST':
        formulario = FormEditarPsicologo(request.POST, instance=user)
        if formulario.is_valid():
            formulario.save()
            return HttpResponseRedirect('/psicologos')
    else:
        formulario = FormEditarPsicologo(instance=user)
    return render(request, 'usuario_editar.html', {'formulario':formulario})

@login_required(login_url='/login/')
@permission_required('ptti.change_psicologo', login_url="/login/")
def desactivar_psicologo(request, user_id):
    user = get_object_or_404(Psicologo, pk=user_id)
    user.desactivar()
    user.save()
    return HttpResponseRedirect('/psicologos')

@login_required(login_url='/login/')
@permission_required('ptti.change_psicologo', login_url="/login/")
def activar_psicologo(request, user_id):
    user = get_object_or_404(Psicologo, pk=user_id)
    user.activar()
    user.save()
    return HttpResponseRedirect('/psicologos')


#vistas para estudiantes

@login_required(login_url='/login/')
@permission_required('ptti.change_estudiante', login_url="/login/")
def estudiantes(request):
    usuarios_lista = Estudiante.objects.order_by('-date_joined').exclude(id=request.user.id)
    context = {'usuarios_lista': usuarios_lista}
    return render(request, 'usuarios.html', context)

def crear_estudiante(request):
    if request.method=='POST':
        formulario = FormCrearEstudiante(request.POST)
        if formulario.is_valid():
            formulario.save(commit=False)
            formulario.save()
            return HttpResponseRedirect('/estudiantes')
    else:
        formulario = FormCrearEstudiante()
    return render(request, 'usuario_crear.html', {'formulario':formulario})

@login_required(login_url='/login')
@permission_required('ptti.change_estudiante', login_url="/login/")
def editar_estudiante(request, user_id):
    user = get_object_or_404(Estudiante, pk=user_id)
    if request.method=='POST':
        formulario = FormEditarEstudiante(request.POST, instance=user)
        if formulario.is_valid():
            formulario.save()
            return HttpResponseRedirect('/estudiantes')
    else:
        formulario = FormEditarEstudiante(instance=user)
    return render(request, 'usuario_editar.html', {'formulario':formulario})

@login_required(login_url='/login/')
@permission_required('ptti.change_estudiante', login_url="/login/")
def desactivar_estudiante(request, user_id):
    user = get_object_or_404(Estudiante, pk=user_id)
    user.desactivar()
    user.save()
    return HttpResponseRedirect('/estudiantes')

@login_required(login_url='/login/')
@permission_required('ptti.change_estudiante', login_url="/login/")
def activar_estudiante(request, user_id):
    user = get_object_or_404(Estudiante, pk=user_id)
    user.activar()
    user.save()
    return HttpResponseRedirect('/estudiantes')

#vistas instituciones

@login_required(login_url='/login/')
@permission_required('ptti.change_institucion', login_url="/login/")
def instituciones(request):
    instituciones_lista = Institucion.objects.order_by('nit')
    context = {'instituciones_lista': instituciones_lista}
    return render(request, 'instituciones.html', context)

@login_required(login_url='/login/')
@permission_required('ptti.add_institucion', login_url="/login/")
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
@permission_required('ptti.change_institucion', login_url="/login/")
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
@permission_required('ptti.change_institucion', login_url="/login/")
def desactivar_institucion(request, ins_id):
    ins = get_object_or_404(Institucion, pk=ins_id)
    ins.desactivar()
    ins.save()
    return HttpResponseRedirect('/instituciones')

@login_required(login_url='/login/')
@permission_required('ptti.change_institucion', login_url="/login/")
def activar_institucion(request, ins_id):
    ins = get_object_or_404(Institucion, pk=ins_id)
    ins.activar()
    ins.save()
    return HttpResponseRedirect('/instituciones')

#vistas para grupos

@login_required(login_url='/login/')
@permission_required('ptti.change_grupo', login_url="/login/")
def grupos(request):
    grupos_lista = Grupo.objects.order_by('nombre')
    context = {'grupos_lista': grupos_lista}
    return render(request, 'grupos.html', context)

@login_required(login_url='/login/')
@permission_required('ptti.add_grupo', login_url="/login/")
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
@permission_required('ptti.change_grupo', login_url="/login/")
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
@permission_required('ptti.change_grupo', login_url="/login/")
def desactivar_grupo(request, gru_id):
    gru = get_object_or_404(Grupo, pk=gru_id)
    gru.desactivar()
    gru.save()
    return HttpResponseRedirect('/grupos')

@login_required(login_url='/login/')
@permission_required('ptti.change_grupo', login_url="/login/")
def activar_grupo(request, gru_id):
    gru = get_object_or_404(Grupo, pk=gru_id)
    gru.activar()
    gru.save()
    return HttpResponseRedirect('/grupos')
