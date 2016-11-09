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
                    if request.user.is_estudiante:
                        return HttpResponseRedirect('/mis-test/')
                    if request.user.is_psicologo:
                        return HttpResponseRedirect('/asignados/')
                    if request.user.is_administrador:
                        return HttpResponseRedirect('/test/')
                    if request.user.is_superuser:
                        return HttpResponseRedirect('/administradores/')
                    #return HttpResponseRedirect('/perfil')
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
    grupos_lista = Grupo.objects.order_by('psicologo')
    usuarios_lista = Psicologo.objects.order_by('-date_joined').exclude(id=request.user.id)
    context = {'usuarios_lista': usuarios_lista,'grupos_lista': grupos_lista}
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
@permission_required('ptti.change_grupo', login_url="/login/")


@login_required(login_url='/login')
@permission_required('ptti.change_grupo', login_url="/login/")
def asignar_psicologo_grupo(request,user_id):
    grupos_lista = Grupo.objects.only('id').filter(psicologo=user_id)
    aux=list(grupos_lista)
    user = get_object_or_404(Usuario, pk=user_id)
    usuario=str(user)
    psi = Psicologo.objects.get(username=usuario)
    if request.method == 'POST':
        grupo_id = request.POST.get("nombre")
        grupo = Grupo.objects.get(pk=grupo_id)
        formulario = FormAsignarPsicologoGrupo(request.POST, instance=grupo)
        if formulario.is_valid():
            formulario.save()
            return HttpResponseRedirect('/psicologos')
        else:
            print formulario.errors
    else:
        formulario = FormAsignarPsicologoGrupo(initial={'psicologo': psi})

    return render(request, 'asignar_psicologo_grupo.html', {'formulario':formulario,'user':usuario})


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
def asignar_grupo_psicologo(request, gru_id):
    gru = get_object_or_404(Grupo, pk=gru_id)
    if request.method == 'POST':
        formulario = FormAsignarGrupoPsicologo(request.POST, instance=gru)
        if formulario.is_valid():
            #ins = formulario.save(commit=False)
            formulario.save()
            return HttpResponseRedirect('/grupos')
    else:
        formulario = FormAsignarGrupoPsicologo(instance=gru)
    return render(request, 'asignar_grupo_psicologo.html', {'formulario':formulario})

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
@permission_required('ptti.change_psicologo', login_url="/login/")
def activar_grupo(request, gru_id):
    gru = get_object_or_404(Grupo, pk=gru_id)
    gru.activar()
    gru.save()
    return HttpResponseRedirect('/grupos')

#vistas de test

@login_required(login_url='/login/')
#@permission_required('ptti.change_test', login_url="/login/")
def testTI(request):
    test_lista = TestTI.objects.order_by('nombre')
    context = {'test_lista': test_lista}
    return render(request, 'test.html', context)

@login_required(login_url='/login/')
#@permission_required('ptti.add_test', login_url="/login/")
def crear_test(request):
    if request.method == 'POST':
        formulario = FormTestTI(request.POST)
        if formulario.is_valid():
            te = formulario.save(commit=False)
            te.save()
            return HttpResponseRedirect('/test')
    else:
        formulario = FormTestTI()
    return render(request, 'test_form.html', {'formulario':formulario})

@login_required(login_url='/login')
#@permission_required('ptti.change_test', login_url="/login/")
def cambiar_nombre_test(request, test_id):
    te = get_object_or_404(TestTI, pk=test_id)
    if request.method == 'POST':
        formulario = FormTestTI(request.POST, instance=te)
        if formulario.is_valid():
            #ins = formulario.save(commit=False)
            formulario.save()
            return HttpResponseRedirect('/test')
    else:
        formulario = FormTestTI(instance=te)
    return render(request, 'test_form.html', {'formulario':formulario})


@login_required(login_url='/login/')
#@permission_required('ptti.change_test', login_url="/login/")
def desactivar_test(request, test_id):
    te = get_object_or_404(TestTI, pk=test_id)
    te.desactivar()
    te.save()
    return HttpResponseRedirect('/test')

@login_required(login_url='/login/')
#@permission_required('ptti.change_test', login_url="/login/")
def activar_test(request, test_id):
    te = get_object_or_404(TestTI, pk=test_id)
    te.activar()
    te.save()
    return HttpResponseRedirect('/test')


#vistas de preguntas

@login_required(login_url='/login/')
#@permission_required('ptti.change_grupo', login_url="/login/")
def preguntas_test(request, test_id):
    pregunta_lista = PreguntaTestTI.objects.order_by('numero').filter(test=test_id)
    context = {'pregunta_lista': pregunta_lista, 'test':test_id}
    return render(request, 'pregunta.html', context)

@login_required(login_url='/login/')
#@permission_required('ptti.change_test', login_url="/login/")
def crear_pregunta(request, test_id):
    if request.method == 'POST':
        formulario = FormPreguntaTestTI(request.POST)
        if formulario.is_valid():
            #ins = formulario.save(commit=False)
            formulario.save()
            test = TestTI.objects.get(pk=test_id)
            test.no_preguntas += 1
            test.save()
            return preguntas_test(request, test_id)
    else:
        formulario = FormPreguntaTestTI()
    return render(request, 'pregunta_form.html', {'formulario':formulario})


@login_required(login_url='/login')
#@permission_required('ptti.change_test', login_url="/login/")
def editar_pregunta(request, pre_id,test_id):
    pre = get_object_or_404(PreguntaTestTI, pk=pre_id)
    if request.method == 'POST':
        formulario = FormPreguntaTestTI(request.POST, instance=pre)
        if formulario.is_valid():
            #ins = formulario.save(commit=False)
            formulario.save()
            return preguntas_test(request, test_id)
    else:
        formulario = FormPreguntaTestTI(instance=pre)
    return render(request, 'pregunta_form.html', {'formulario':formulario})


# vistas  de repuestas
@login_required(login_url='/login')
#@permission_required('ptti.change_test', login_url="/login/")
def respuestas_pregunta(request, pre_id):
    respuesta_lista = RespuestaTestTI.objects.order_by('respuesta').filter(pregunta=pre_id)
    context = {'respuesta_lista': respuesta_lista, 'pregunta':pre_id}
    return render(request, 'respuesta.html', context)


@login_required(login_url='/login')
#@permission_required('ptti.change_test', login_url="/login/")
def crear_respuesta(request, pre_id):
    if request.method == 'POST':
        formulario = FormRespuestaTestTI(request.POST)
        if formulario.is_valid():
            #ins = formulario.save(commit=False)
            formulario.save()
            return respuestas_pregunta(request, pre_id)
    else:
        formulario = FormRespuestaTestTI()
    return render(request, 'respuesta_form.html', {'formulario':formulario})


@login_required(login_url='/login')
#@permission_required('ptti.change_test', login_url="/login/")
def editar_respuesta(request, res_id,pre_id):
    res = get_object_or_404(RespuestaTestTI, pk=res_id)
    if request.method == 'POST':
        formulario = FormRespuestaTestTI(request.POST, instance=res)
        if formulario.is_valid():
            #ins = formulario.save(commit=False)
            formulario.save()
            return respuestas_pregunta(request, pre_id)
    else:
        formulario = FormRespuestaTestTI(instance=res)
    return render(request, 'respuesta_form.html', {'formulario':formulario})


#######################    vistas del psicologo           #######################

# vistas para asignacion de test

@login_required(login_url='/login')
#@permission_required('ptti.asignar', login_url="/login/")
def TestAsignados(request):
    lista = TestAsignado.objects.filter(estudiante__grupo__psicologo=request.user)
    context = {'asignados_lista': lista}
    return render(request, 'testAsignados.html', context)


@login_required(login_url='/login')
#@permission_required('ptti.change_grupo', login_url="/login/")
def asignarTestEstudiante(request):
    if request.method == 'POST':
        formulario = FormAsignartestEstudiante(request.POST,psicol=request.user)
        if formulario.is_valid():
            gru = formulario.save(commit=False)
            gru.save()
            return HttpResponseRedirect('/asignados')
    else:
        formulario = FormAsignartestEstudiante(psicol=request.user)
    return render(request, 'asignar_test_estudiante.html', {'formulario':formulario})

@login_required(login_url='/login')
def asignarTestGrupo(request):
    grupos_lista = Grupo.objects.filter(psicologo=request.user)
    context = {'grupos_lista': grupos_lista}
    return render(request, 'asignar_test_grupo.html', context)


@login_required(login_url='/login')
def listaEstudiantes(request, gru_id):
    if request.method == 'POST':
        formulario = FormAsignartestEstudianteGrupo(request.POST,grupo=gru_id)
        if formulario.is_valid():
            gru = formulario.save(commit=False)
            gru.save()
            return HttpResponseRedirect('/asignados/asignarTestGrupo')
    else:
        formulario = FormAsignartestEstudianteGrupo(grupo=gru_id)
    return render(request, 'asignar_test_estudiante.html', {'formulario':formulario})


"""
@login_required(login_url='/login')
#@permission_required('ptti.change_grupo', login_url="/login/")
def asigna
rTestGrupo(request,user_id):
    asignados_lista = Grupo.objects.filter(psicologo=user_id)
    context = {'asignados_lista': asignados_lista, 'user':user_id}
    return render(request, 'testAsignados.html', context)
# vistas de diagnostico
@login_required(login_url='/login')
#@permission_required('ptti.diagnosticar', login_url="/login/")
def diagnosticar(request):
    return render(request, 'diagnosticar.html')
"""

# vistas para estudiantes

@login_required(login_url='/login')
#@permission_required('ptti.asignar', login_url="/login/")
def TestEstudiante(request):
    estudiante = Estudiante.objects.filter(pk=request.user.id)
    lista_test = TestAsignado.objects.filter(estudiante=estudiante)
    context = {'asignados_lista': lista_test}
    return render(request, 'mis-test.html', context)

@login_required(login_url='/login')
def IniciarTest(request,id_test_asi):
    test_asi    = get_object_or_404(TestAsignado, pk=id_test_asi)
    test = get_object_or_404(TestTI, pk=test_asi.id)
    return render(request, 'responder_test.html', {'test': test})

@login_required(login_url='/login')
def ResponderTest(request,id_test_asi,no_preg):
    test_asi    = get_object_or_404(TestAsignado, pk=id_test_asi)
    test_asi.cambiaEstado("INICIADO")
    test_asi.pre_actual = no_preg
    test_asi.save()
    test        = get_object_or_404(TestTI, pk=test_asi.id)
    pregunta    = get_object_or_404(PreguntaTestTI,test=test.id, numero=no_preg)
    respuestas  = RespuestaTestTI.objects.filter(pregunta=pregunta)

    if request.method == 'POST':
        try:
            rs = pregunta.respuestatestti_set.get(pk=request.POST['rs'])
        except (KeyError, RespuestaTestTI.DoesNotExist):
            return render(request, 'responder_pregunta.html', {
                'test':test_asi,
                'pregunta':pregunta,
                'respuestas':respuestas,
                'error_message': "No ha seleccionado una opcion",
            })
        else:
            siguiente = int(no_preg) + 1

            obj = RespuestaEstudiante.objects.get(
                testAsignado = test_asi,
                pregunta = pregunta,
            )
            obj.respuesta = rs
            obj.save()

            if siguiente <= test.no_preguntas:
                return HttpResponseRedirect(reverse('ptti:ResponderTest', args=(id_test_asi,str(siguiente))))
            else:
                test_asi.cambiaEstado("FINALIZADO")
                test_asi.pre_actual = test.no_preguntas
                test_asi.save()
                #return HttpResponseRedirect(reverse('ptti:TerminarTest', args=(id_test_asi,)))
                return HttpResponseRedirect(reverse('ptti:TestEstudiante'))
    else:
        return render(request, 'responder_pregunta.html', {
            'test':test,
            'pregunta':pregunta,
            'respuestas':respuestas
        })

"""
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
"""


@login_required(login_url='/login')
def TerminarTest(request,id_test_asi):
    pass
