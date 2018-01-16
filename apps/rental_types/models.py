"""
    Created by: @pdonaire1
    Pablo Gonzalez Donaire
"""
from django.db import models

class RentalType(models.Model):
    """
    Type of Rental
    """
    amount = models.FloatField()
    # Duration of the retal
    length = models.CharField(max_length=80)

    def __str__(self):
        return '{0}$ per {1}'.format(self.amount, self.length)
