from django.db import models
from django.contrib.auth.models import User
from main.models import Restaurant  # Assuming your Restaurant model is in the 'main' app

class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)  

    class Meta:
        unique_together = ('user', 'restaurant') 

    def __str__(self):
        return f"{self.user.username} - {self.restaurant.name}"
