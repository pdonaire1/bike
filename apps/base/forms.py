"""
    @author @pdonaire1
    Pablo Gonzlez Donaire
"""
from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User, Group
from django.forms.fields import (
    CharField, BooleanField
)
from django.forms.widgets import (
    PasswordInput, CheckboxInput, Select
)

class LoginForm(forms.Form):
    """!
    Clase del formulario de logeo

    @author Rodrigo Boet (rudmanmrrod at gmail)
    @date 01-03-2017
    """
    ## Campo de la constraseña
    contrasena = CharField()

    ## Nombre del usuario
    usuario = CharField()

    ## Formulario de recordarme
    remember_me = BooleanField()


    def __init__(self, *args, **kwargs):
        """!
        Metodo que sobreescribe cuando se inicializa el formulario

        @author Rodrigo Boet (rudmanmrrod at gmail)
        @date 01-03-2017
        @param self <b>{object}</b> Objeto que instancia la clase
        @param args <b>{list}</b> Lista de los argumentos
        @param kwargs <b>{dict}</b> Diccionario con argumentos
        @return Retorna el formulario validado
        """
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields['contrasena'].widget = PasswordInput()
        self.fields['contrasena'].widget.attrs.update({'class': 'form-control',
        'placeholder': 'Contraseña'})
        self.fields['usuario'].widget.attrs.update({'class': 'form-control',
        'placeholder': 'Nombre de Usuario'})
        self.fields['remember_me'].label = "Recordar"
        self.fields['remember_me'].widget = CheckboxInput()
        self.fields['remember_me'].required = False

    def clean(self):
        """!
        Método que valida si el usuario a autenticar es valido

        @author Rodrigo Boet (rudmanmrrod at gmail)
        @date 21-04-2017
        @param self <b>{object}</b> Objeto que instancia la clase
        @return Retorna el campo con los errores
        """
        usuario = self.cleaned_data['usuario']
        contrasena = self.cleaned_data['contrasena']
        usuario = authenticate(username=usuario,password=contrasena)
        if(not usuario):
            msg = "Verifique su usuario o contraseña"
            self.add_error('usuario', msg)

    class Meta:
        fields = ('usuario', 'contrasena', 'remember_me')
