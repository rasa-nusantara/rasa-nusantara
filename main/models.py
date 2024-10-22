from django.db import models
import uuid

class Restaurant(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    address = models.TextField()
    rating = models.CharField(max_length=255)
    harga_rata_rata = models.IntegerField()

    def __str__(self):
        return self.name

class Menu(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='menus')
    name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name} - {self.restaurant.name}"
