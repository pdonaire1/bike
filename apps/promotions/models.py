"""
    Created by: @pdonaire1
    Pablo Gonzalez Donaire
"""
from django.db import models

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
