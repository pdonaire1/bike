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
    Class to login form
    """
    ## Campo de la constraseña
    contrasena = CharField()

    ## Nombre del usuario
    usuario = CharField()

    ## Formulario de recordarme
    remember_me = BooleanField()


    def __init__(self, *args, **kwargs):
        """!
        Method that overwritewhen is initalized the form
        @return valid form
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
        Method that validate user
        @return the fields with errors
        """
        usuario = self.cleaned_data['usuario']
        contrasena = self.cleaned_data['contrasena']
        usuario = authenticate(username=usuario,password=contrasena)
        if(not usuario):
            msg = "Verify your user or password"
            self.add_error('usuario', msg)

    class Meta:
        fields = ('usuario', 'contrasena', 'remember_me')
