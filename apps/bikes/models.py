"""
    Created by: @pdonaire1
    Pablo Gonzalez Donaire
"""
from django.db import models

class Bike(models.Model):
    """
    Class that allow to clients rents bikes
    """
    ROAD = 'ROAD'
    MOUNTAIN = 'MOUNTAIN'
    TRAVEL = 'TRAVEL'
    ELECTRIC = 'ELECTRIC'
    BIKE_TYPE_CHOICES = (
        (ROAD, 'Road'),
        (MOUNTAIN, 'Mountain'),
        (TRAVEL, 'Travel'),
        (ELECTRIC, 'Electric'),
    )
    bike_code = models.CharField(max_length=80)
    bike_type = models.CharField(
        max_length=10,
        choices=BIKE_TYPE_CHOICES,
        default=TRAVEL)
    available = models.BooleanField(default=True)

    def __str__(self):
        return str(self.bike_code) + ' ' + str(self.bike_type)
