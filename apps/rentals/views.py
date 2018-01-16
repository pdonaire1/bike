"""
    @author @pdonaire1
    Pablo Gonzlez Donaire
"""
from django.shortcuts import render
from django.views.generic import FormView, RedirectView
from rentals.forms import NewRentalForm, ClientForm
from django.views.generic import TemplateView
from django.core.urlresolvers import reverse_lazy
from bikes.models import Bike
from rentals.models import RentalType, Promotion
from django.core import serializers
from django.utils.safestring import mark_safe
from django.http import HttpResponse
# class NewRentalView(FormView):
#     """
#     View that make the login of the platform
#     """
#     form_class = NewRentalForm
#     template_name = 'rentals/new_rental.html'
#     success_url = reverse_lazy('index')
#
#     def form_valid(self, form):
#         """
#         Method that validate the form
#         """
#         # usuario = form.cleaned_data['usuario']
#         # contrasena = form.cleaned_data['contrasena']
#         # usuario = authenticate(username=usuario, password=contrasena)
#         # if usuario.is_superuser or User.objects.filter(pk=usuario.id, groups__name='Administrador').exists():
#         #     login(self.request, usuario)
#         #     if self.request.POST.get('remember_me') is not None:
#         #         # Session expira a los dos meses si no se deslogea
#         #         self.request.session.set_expiry(1209600)
#         return super(NewRentalView, self).form_valid(form)


class NewRentalView(TemplateView):
    template_name = "rentals/new_rental.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['from_client'] = ClientForm
        bikes = Bike.objects.filter(available=True).values()
        rental_types = RentalType.objects.all().values()
        promotions = Promotion.objects.all().values()
        context['promotions'] = mark_safe(promotions)
        context['rental_types'] = mark_safe(rental_types)
        context['bikes_available'] = mark_safe(bikes)
        return context

    def post(self, request, *args, **kwargs):
        print (self.request.POST)
        phone = self.request.POST.get('phone')
        full_name = self.request.POST.get('full_name')
        address = self.request.POST.get('address')
        if Client.objects.filter(phone=phone).exists():
            client = Client.objects.get(phone=phone)
        else:
            client = Client(phone=phone)
        client.full_name = full_name
        client.address = address
        client.save()
        

        return HttpResponse('Hello, World!')
