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
from rentals.models import RentalType
from bikes.models import Bike

class ClientForm(forms.Form):
    """
    Simple form of client model
    """
    phone = CharField()
    full_name = CharField()
    address = CharField()

    def __init__(self, *args, **kwargs):
        """
        @return Return the valid form
        """
        super(ClientForm, self).__init__(*args, **kwargs)
        #self.fields['contrasena'].widget = PasswordInput()
        #self.fields['contrasena'].widget.attrs.update({'class': 'form-control',
        #'placeholder': 'Contraseña'})
        self.fields['phone'].widget.attrs.update({'class': 'form-control',
        'placeholder': 'Phone Number'})
        self.fields['full_name'].widget.attrs.update({'class': 'form-control',
        'placeholder': 'Full Name'})
        self.fields['address'].widget.attrs.update({'class': 'form-control',
        'placeholder': 'Address'})

class NewRentalForm(forms.Form):
    """!
    New Rental django form class

    Cuando el usuario mete el telefono deberian
    aparecer los datos del cliente, si no es asi entonces
    el formulario de los datos del cliente queda vacio.
    y se llena el resto de los campos foraneos.

    Nota el cliente lo consulta del telefono de la tabla client
    Nota 2: Se verifica si el registro tiene bicicletas con promociones
    y se le asigna la promocion
    """
    # Client Data
    full_name = CharField()
    phone = CharField()
    address = CharField()
    # Rental Data:
    rental_type = forms.Select()
    bike = Select()
    #promotion = Select()


    def __init__(self, *args, **kwargs):
        """
        @return Return the valid form
        """
        super(NewRentalForm, self).__init__(*args, **kwargs)
        #self.fields['contrasena'].widget = PasswordInput()
        #self.fields['contrasena'].widget.attrs.update({'class': 'form-control',
        #'placeholder': 'Contraseña'})
        self.fields['usuario'].widget.attrs.update({'class': 'form-control',
        'placeholder': 'Nombre de Usuario'})

        RENTAL_TYPE_CHOICES = [(i.id, i.__str__()) for i in RentalType.objects.all()]
        self.fields['rental_type'].widget = forms.Select(choices=RENTAL_TYPE_CHOICES)
        BIKE_CHOICES = [(i.id, i.__str__()) for i in Bike.objects.filter(available=True)]
        self.fields['bike'].widget = forms.Select(choices=BIKE_CHOICES)


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
        fields = ('full_name', 'phone', 'address')
