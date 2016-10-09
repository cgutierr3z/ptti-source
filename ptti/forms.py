from django import forms
from django.contrib.auth.models import User
from .models import *
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, ReadOnlyPasswordHashField

class FormCrearUsuario(UserCreationForm):
    TIPO_DOC_LIST = [
        ('CC', 'CEDULA CUIDADANIA'),
        ('CE', 'CEDULA EXTRANJERIA'),
        ('PAS', 'PASAPORTE'),
        ('TI', 'TARJETA IDENTIDAD'),
    ]
    GENERO_LIST= [
        ('HT', 'HETEROSEXUAL'),
        ('HM', 'HOMOSEXUAL'),
        ('LE', 'LESBIANA'),
        ('BI', 'BISEXUAL'),
        ('IN', 'INDIFERENCIADO'),
    ]
    email       = forms.EmailField(label='Correo electronico',required=True)
    first_name  = forms.CharField(label='Nombres',required=True)
    last_name   = forms.CharField(label='Apellidos',required=True)
    tipo_docto  = forms.ChoiceField(label='Tipo documento',choices = TIPO_DOC_LIST, initial='', widget=forms.Select(), required=True)
    no_docto    = forms.CharField(label='Numero documento',required=True)
    fecha_nac   = forms.DateField(label='Fecha nacimiento',widget=forms.SelectDateWidget(years=[y for y in range(1990,2017)]),required=True)
    genero      = forms.ChoiceField(label='Genero',choices = GENERO_LIST, initial='', widget=forms.Select(), required=True)
    direccion   = forms.CharField(label='Direccion',required=True)
    telefono    = forms.CharField(label='Telefono',required=True)
    is_active       = forms.BooleanField(label='Activo',required=False)
    is_administrador= forms.BooleanField(label='Administrador',required=False)
    is_psicologo    = forms.BooleanField(label='Psicologo',required=False)
    is_estudiante   = forms.BooleanField(label='Estudiante',required=False)


    class Meta:
        model = Usuario
        fields = ('username','email','first_name','last_name','tipo_docto','no_docto','fecha_nac','genero','direccion','telefono','password1', 'password2','is_active','is_administrador','is_psicologo','is_estudiante')

    def save(self, commit=True):
        user = super(FormNuevoUsuario, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

class FormEditarUsuario(UserChangeForm):
    fecha_nac   = forms.DateField(label='Fecha nacimiento',widget=forms.SelectDateWidget(years=[y for y in range(1990,2017)]),required=True)
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = Usuario
        fields = ('username','email','first_name','last_name','tipo_docto','no_docto','fecha_nac','genero','direccion','telefono','is_active','is_administrador','is_psicologo','is_estudiante')


    def __init__(self, *args, **kwargs):
        super(FormEditarUsuario, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance and instance.id:
            self.fields['username'].required = False
            self.fields['username'].widget.attrs['disabled'] = 'disabled'

    def clean_username(self):
        # As shown in the above answer.
        instance = getattr(self, 'instance', None)
        if instance:
            try:
                self.changed_data.remove('username')
            except ValueError, e:
                pass
            return instance.username
        else:
            return self.cleaned_data.get('username', None)

    def clean_password(self):
        # As shown in the above answer.
        instance = getattr(self, 'instance', None)
        if instance:
            try:
                self.changed_data.remove('password')
            except ValueError, e:
                pass
            return instance.password
        else:
            return self.cleaned_data.get('password', None)

class FormEditarPerfil(UserChangeForm):
    fecha_nac   = forms.DateField(label='Fecha nacimiento',widget=forms.SelectDateWidget(years=[y for y in range(1990,2017)]),required=True)
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = Usuario
        fields = ('username','email','first_name','last_name','tipo_docto','no_docto','fecha_nac','genero','direccion','telefono','password')


    def __init__(self, *args, **kwargs):
        super(FormEditarPerfil, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance and instance.id:
            self.fields['username'].required = False
            self.fields['username'].widget.attrs['disabled'] = 'disabled'

    def clean_username(self):
        # As shown in the above answer.
        instance = getattr(self, 'instance', None)
        if instance:
            try:
                self.changed_data.remove('username')
            except ValueError, e:
                pass
            return instance.username
        else:
            return self.cleaned_data.get('username', None)

    def clean_password(self):
        # As shown in the above answer.
        instance = getattr(self, 'instance', None)
        if instance:
            try:
                self.changed_data.remove('password')
            except ValueError, e:
                pass
            return instance.password
        else:
            return self.cleaned_data.get('password', None)

class FormInstitucion(forms.ModelForm):
    # nit         = models.CharField(max_length=200,unique=True)
    # nombre      = models.CharField(max_length=200)
    # direccion   = models.CharField(max_length=200)
    # telefono    = models.CharField(max_length=200)
    # cuidad      = models.CharField(max_length=200)
    # web         = models.URLField(max_length=200)

    class Meta:
        model = Institucion
        fields = ['nit', 'nombre', 'direccion','telefono','ciudad','web','is_active']

class FormGrupo(forms.ModelForm):
    class Meta:
        model = Grupo
        fields = ['institucion', 'jornada', 'grado','nombre','is_active']
