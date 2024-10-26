from django.db import models
from django.contrib.auth.models import User
from main.models import Restaurant

class Rating(models.Model):
    restaurant = models.ForeignKey(Restaurant, related_name='ratings', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.PositiveSmallIntegerField()  

    # class Meta:
    #     unique_together = ('restaurant', 'user')  # Satu pengguna hanya bisa memberikan satu rating per restoran

    def __str__(self):
        return f"{self.user.username} - {self.restaurant.name}: {self.score}"