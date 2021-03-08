from django.db import models

from datetime import *

# Create your models here.
#for measurements

class Measurements(models.Model):
    location=models.CharField(max_length=240)
    destination=models.CharField(max_length=240)
    distance=models.DecimalField(max_digits=10,decimal_places=2)
    created=models.DateTimeField(auto_now_add=True)
    class Meta:
        verbose_name_plural="Measurements"

    def __str__(self):
        return f"Distance from {self.location} to {self.destination} is {self.distance} km"


