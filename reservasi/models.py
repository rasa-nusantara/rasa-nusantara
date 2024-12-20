from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from main.models import Restaurant  # Assuming you have the Restaurant model in the 'main' app

class Reservation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # The user making the reservation
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)  # The restaurant being reserved
    reservation_date = models.DateField()  # The date of the reservation
    reservation_time = models.TimeField()  # The time of the reservation
    number_of_people = models.PositiveIntegerField()  # Number of people for the reservation
    special_request = models.TextField(blank=True, null=True)  # Optional special requests

    def __str__(self):
        return f'{self.user.username} - {self.restaurant} on {self.reservation_date} at {self.reservation_time}'
