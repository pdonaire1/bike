"""
    @author @pdonaire1
    Pablo Gonzlez Donaire
"""
from django.shortcuts import render
from django.views.generic import FormView, RedirectView
from rentals.forms import NewRentalForm, ClientForm
from django.views.generic import TemplateView, DetailView, DeleteView
from django.core.urlresolvers import reverse_lazy
from bikes.models import Bike
from clients.models import Client
from rentals.models import RentalType, Promotion, Rental, BikeRental
from django.core import serializers
from django.utils.safestring import mark_safe
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin

class NewRentalView(LoginRequiredMixin, TemplateView):
    login_url = reverse_lazy('login')
    redirect_field_name = 'redirect_to'
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
        phone = self.request.POST.get('phone', None)
        full_name = self.request.POST.get('full_name', None)
        address = self.request.POST.get('address', None)
        if not phone or not full_name or not address:
            messages.add_message(request, messages.ERROR, 'Error: you have to fill all fields')
            return HttpResponseRedirect(reverse_lazy('new-rental'))

        if Client.objects.filter(phone=phone).exists():
            client = Client.objects.get(phone=phone)
        else:
            client = Client(phone=phone)
        client.full_name = full_name
        client.address = address
        client.save()

        index = 0
        data  = []
        while True:
            try:
                data.append({
                    "rental_type_id": self.request.POST['rental_types-' + str(index)],
                    "bike_id": self.request.POST['bike_code-' + str(index)]
                })
                index += 1
            except: break
        data_count = len(data)
        # Verifying if there are some promotion available for the number of bikes
        promotion = Promotion.objects.filter(
            count_rental_to__gte=data_count,
            count_rental_from__lte=data_count).first()
        rental = Rental(client=client, promotion=promotion)
        rental.save()

        # Let's save the all the bikes in the invoice
        for d in data:
            bike_rental = BikeRental(
                rental_type=RentalType.objects.get(id=d['rental_type_id']),
                bike=Bike.objects.get(id=d['bike_id']),
                rental=rental)
            bike_rental.save()

        messages.add_message(request, messages.INFO, 'Rental Successfully Created')
        return HttpResponseRedirect(reverse_lazy('index'))

class RentalDetailView(LoginRequiredMixin, DetailView):
    login_url = reverse_lazy('login')
    redirect_field_name = 'redirect_to'
    model = Rental
    template_name = 'rentals/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['bike_rentals'] = BikeRental.objects.filter(rental__id=context['object'].id)
        return context

    def post(self, request, pk, *args, **kwargs):
        rental = Rental.objects.get(id=pk)
        rental.finished = True
        rental.save()
        messages.add_message(request, messages.INFO, 'Rental status has been Finished')
        return HttpResponseRedirect(reverse_lazy('index'))

class RentalDeleteView(LoginRequiredMixin, DeleteView):
    """
    Class to delete the Rentail object
    """
    login_url = reverse_lazy('login')
    redirect_field_name = 'redirect_to'
    model = Rental
    template_name = "rentals/rental_delete.html"
    success_message = "Rental was successfully deleted"
    success_url = reverse_lazy('index')

    def get_object(self, **kwargs):
    	"""!
    	Return the rental object
    	"""
    	return Rental.objects.get(id=int(self.kwargs['pk']))
