"""
    Created by: @pdonaire1
    Pablo Gonzalez Donaire
"""
from django.db import models

class Client(models.Model):
	"""
	Client Class for rental bikes
	"""

	full_name = models.CharField(max_length=80)
	phone = models.CharField(max_length=80)
	address = models.CharField(max_length=250)

	def __str__(self):
		return str(self.full_name)
