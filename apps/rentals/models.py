"""
    Created by: @pdonaire1
    Pablo Gonzalez Donaire
"""
from django.db import models
from bikes.models import Bike
from clients.models import Client

class Promotion(models.Model):
    """
    Promotion of Rental
    """
    # Range of bikes in promotion, example:
    # Family Rental, is a promotion that can include from 3 to 5 Rentals (of any type) with a discount of 30% of the total price
    count_rental_from = models.IntegerField()
    count_rental_to = models.IntegerField()

    percentaje_discount = models.IntegerField()
    name = models.CharField(max_length=80)

    def __str__(self):
        return str(self.name)


class RentalType(models.Model):
    """
    Type of Rental
    """
    amount = models.FloatField()
    # Duration of the retal
    length = models.CharField(max_length=80)

    def __str__(self):
        return '{0}$ per {1}'.format(self.amount, self.length)


class Rental(models.Model):
	"""
	Class to make a Rental or invoice
	"""
    # Range of bikes in promotion, example:
    # Family Rental, is a promotion that can include from 3 to 5 Rentals (of any type) with a discount of 30% of the total price
	client = models.ForeignKey(Client)
	promotion = models.ForeignKey(Promotion)

	def __str__(self):
		return str(self.name)


class BikeRental(models.Model):
    """
    Class beetween Bike and Rentals for invoices
    """
    bike = models.ForeignKey(Bike)
    rental = models.ForeignKey(Rental)
    rental_type = models.ForeignKey(RentalType)

    def __str__(self):
        return str(self.id)
