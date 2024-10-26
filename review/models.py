from django.db import models
from django.contrib.auth.models import User


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Review terkait dengan user
    restaurant_name = models.CharField(max_length=255)  # Nama restoran (ambil dari dummy data)
    rating = models.PositiveSmallIntegerField()  # Rating dari 1-5
    comment = models.TextField()  # Komentar pengguna
    created_at = models.DateTimeField(auto_now_add=True)  # Waktu review dibuat

    def __str__(self):
        return f"Review by {self.user.username} for {self.restaurant_name}"
