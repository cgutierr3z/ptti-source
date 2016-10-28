from django import forms
from django.contrib.auth.models import User
from .models import *
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, ReadOnlyPasswordHashField
from django.contrib.auth.models import Group

TIPO_DOC_LIST = [
    ('CEDULA CUIDADANIA', 'CEDULA CUIDADANIA'),
    ('CEDULA EXTRANJERIA', 'CEDULA EXTRANJERIA'),
    ('PASAPORTE', 'PASAPORTE'),
    ('TARJETA IDENTIDAD', 'TARJETA IDENTIDAD'),
]
GENERO_LIST= [
    ('HETEROSEXUAL', 'HETEROSEXUAL'),
    ('HOMOSEXUAL', 'HOMOSEXUAL'),
    ('LESBIANA', 'LESBIANA'),
    ('BISEXUAL', 'BISEXUAL'),
    ('INDIFERENCIADO', 'INDIFERENCIADO'),
]

class FormCrearUsuario(UserCreationForm):
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

    class Meta:
        model = Usuario
        fields = ('username','email','first_name','last_name','tipo_docto','no_docto','fecha_nac','genero','direccion','telefono','password1', 'password2','is_active','is_administrador','is_psicologo')

    def save(self, commit=True):
        user = super(FormCrearUsuario, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            if user.is_administrador:
                user.groups.add(Group.objects.get(name='administrador'))
            if user.is_psicologo:
                user.groups.add(Group.objects.get(name='psicologo'))
            user.save()
        return user

class FormEditarUsuario(UserChangeForm):
    fecha_nac   = forms.DateField(label='Fecha nacimiento',widget=forms.SelectDateWidget(years=[y for y in range(1990,2017)]),required=True)
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = Usuario
        fields = ('username','email','first_name','last_name','tipo_docto','no_docto','fecha_nac','genero','direccion','telefono','is_active','is_administrador','is_psicologo','password')

    def save(self, commit=True):
        user = super(FormEditarUsuario, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if user.is_administrador:
            user.groups.add(Group.objects.get(name='administrador'))
        else:
            user.groups.remove(Group.objects.get(name='administrador'))
        if user.is_psicologo:
            user.groups.add(Group.objects.get(name='psicologo'))
        else:
            user.groups.remove(Group.objects.get(name='psicologo'))
        if commit:
            user.save()
        return user

    def __init__(self, *args, **kwargs):
        super(FormEditarUsuario, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance and instance.id:
            self.fields['username'].required = False
            self.fields['username'].widget.attrs['disabled'] = 'disabled'

    def clean_username(self):
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
        instance = getattr(self, 'instance', None)
        if instance:
            try:
                self.changed_data.remove('password')
            except ValueError, e:
                pass
            return instance.password
        else:
            return self.cleaned_data.get('password', None)

class FormCrearAdministrador(UserCreationForm):
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

    class Meta:
        model = Administrador
        fields = ('username','email','first_name','last_name','tipo_docto','no_docto','fecha_nac','genero','direccion','telefono','password1', 'password2','is_active','is_administrador','is_psicologo')

    def save(self, commit=True):
        user = super(FormCrearAdministrador, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            user.groups.add(Group.objects.get(name='administrador'))
            user.save()
        return user

class FormEditarAdministrador(UserChangeForm):
    fecha_nac   = forms.DateField(label='Fecha nacimiento',widget=forms.SelectDateWidget(years=[y for y in range(1990,2017)]),required=True)
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = Administrador
        fields = ('username','email','first_name','last_name','tipo_docto','no_docto','fecha_nac','genero','direccion','telefono','is_active','is_administrador','is_psicologo','password')

    def save(self, commit=True):
        user = super(FormEditarAdministrador, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if user.is_administrador:
            user.groups.add(Group.objects.get(name='administrador'))
        else:
            user.groups.remove(Group.objects.get(name='administrador'))
        if user.is_psicologo:
            user.groups.add(Group.objects.get(name='psicologo'))
        else:
            user.groups.remove(Group.objects.get(name='psicologo'))
        if commit:
            user.save()
        return user

    def __init__(self, *args, **kwargs):
        super(FormEditarAdministrador, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance and instance.id:
            self.fields['username'].required = False
            self.fields['username'].widget.attrs['disabled'] = 'disabled'

    def clean_username(self):
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
        instance = getattr(self, 'instance', None)
        if instance:
            try:
                self.changed_data.remove('password')
            except ValueError, e:
                pass
            return instance.password
        else:
            return self.cleaned_data.get('password', None)

class FormCrearPsicologo(UserCreationForm):
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

    class Meta:
        model = Psicologo
        fields = ('username','email','first_name','last_name','tipo_docto','no_docto','fecha_nac','genero','direccion','telefono','password1', 'password2','is_active','is_administrador','is_psicologo')

    def save(self, commit=True):
        user = super(FormCrearPsicologo, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            user.groups.add(Group.objects.get(name='psicologo'))
            user.save()
        return user

class FormEditarPsicologo(UserChangeForm):
    fecha_nac   = forms.DateField(label='Fecha nacimiento',widget=forms.SelectDateWidget(years=[y for y in range(1990,2017)]),required=True)
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = Psicologo
        fields = ('username','email','first_name','last_name','tipo_docto','no_docto','fecha_nac','genero','direccion','telefono','is_active','is_administrador','is_psicologo','password')

    def save(self, commit=True):
        user = super(FormEditarPsicologo, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if user.is_administrador:
            user.groups.add(Group.objects.get(name='administrador'))
        else:
            user.groups.remove(Group.objects.get(name='administrador'))
        if user.is_psicologo:
            user.groups.add(Group.objects.get(name='psicologo'))
        else:
            user.groups.remove(Group.objects.get(name='psicologo'))
        if commit:
            user.save()
        return user

    def __init__(self, *args, **kwargs):
        super(FormEditarPsicologo, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance and instance.id:
            self.fields['username'].required = False
            self.fields['username'].widget.attrs['disabled'] = 'disabled'

    def clean_username(self):
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
        instance = getattr(self, 'instance', None)
        if instance:
            try:
                self.changed_data.remove('password')
            except ValueError, e:
                pass
            return instance.password
        else:
            return self.cleaned_data.get('password', None)

class FormCrearEstudiante(UserCreationForm):
    email       = forms.EmailField(label='Correo electronico',required=True)
    first_name  = forms.CharField(label='Nombres',required=True)
    last_name   = forms.CharField(label='Apellidos',required=True)
    tipo_docto  = forms.ChoiceField(label='Tipo documento',choices = TIPO_DOC_LIST, initial='', widget=forms.Select(), required=True)
    no_docto    = forms.CharField(label='Numero documento',required=True)
    fecha_nac   = forms.DateField(label='Fecha nacimiento',widget=forms.SelectDateWidget(years=[y for y in range(1990,2017)]),required=True)
    genero      = forms.ChoiceField(label='Genero',choices = GENERO_LIST, initial='', widget=forms.Select(), required=True)
    direccion   = forms.CharField(label='Direccion',required=True)
    telefono    = forms.CharField(label='Telefono',required=True)
    is_active   = forms.BooleanField(label='Activo',required=False)

    class Meta:
        model = Estudiante
        fields = ('username','email','first_name','last_name','grupo','tipo_docto','no_docto','fecha_nac','genero','direccion','telefono','password1', 'password2','is_active')

    def save(self, commit=True):
        user = super(FormCrearEstudiante, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.is_estudiante = True

        if commit:
            user.save()
            user.groups.add(Group.objects.get(name='estudiante'))
            user.save()

        return user

class FormEditarEstudiante(UserChangeForm):
    fecha_nac   = forms.DateField(label='Fecha nacimiento',widget=forms.SelectDateWidget(years=[y for y in range(1990,2017)]),required=True)
    password    = ReadOnlyPasswordHashField()

    class Meta:
        model = Estudiante
        fields = ('username','email','first_name','last_name','grupo','tipo_docto','no_docto','fecha_nac','genero','direccion','telefono','is_active','password')

    def save(self, commit=True):
        user = super(FormEditarEstudiante, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if user.is_estudiante:
            user.groups.add(Group.objects.get(name='estudiante'))
        else:
            user.groups.remove(Group.objects.get(name='estudiante'))
        if commit:
            user.save()
        return user

    def __init__(self, *args, **kwargs):
        super(FormEditarEstudiante, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance and instance.id:
            self.fields['username'].required = False
            self.fields['username'].widget.attrs['disabled'] = 'disabled'

    def clean_username(self):
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
    class Meta:
        model = Institucion
        fields = ['nit', 'nombre', 'direccion','telefono','ciudad','web','is_active']

class FormGrupo(forms.ModelForm):
    class Meta:
        model = Grupo
        fields = ['institucion', 'jornada', 'grado','nombre','psicologo','is_active']

class FormTestTI(forms.ModelForm):
    class Meta:
        model = TestTI
        fields = ['nombre']

class FormPreguntaTestTI(forms.ModelForm):
    class Meta:
        model = PreguntaTestTI
        fields = ['test','pregunta','numero']

class FormRespuestaTestTI(forms.ModelForm):
    class Meta:
        model = RespuestaTestTI
        fields = ['pregunta','respuesta']

class FormTestAsignado(forms.ModelForm):
    class Meta:
        model = TestAsignado
        fields = ['estudiante','test','estado']

class FormAsignarGrupoPsicologo(forms.ModelForm):
    class Meta:
        model = Grupo
        fields = ['nombre','psicologo']

class FormAsignarPsicologoGrupo(forms.ModelForm):
    nombre = forms.ModelChoiceField(label='Nombre del grupo', queryset=Grupo.objects.all().filter(psicologo=None))
    psicologo= forms.ModelChoiceField(label='Nombre del psicologo', queryset=Psicologo.objects.filter(is_active=True))
    class Meta:
        model = Grupo
        fields = ['nombre','psicologo']
    

