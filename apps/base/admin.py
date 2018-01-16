from django.contrib import admin
from bikes.models import Bike
from clients.models import Client
from rentals.models import Rental, RentalType, Promotion

admin.site.register(Bike)
admin.site.register(Client)
admin.site.register(Promotion)
admin.site.register(Rental)
admin.site.register(RentalType)
