from django.db import models
from django.contrib.auth.models import User
from adminview.models import Restaurant  # Ini adalah model restoran yang akan di-favoritkan

class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='favorited_by')
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name