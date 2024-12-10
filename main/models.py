from django.db import models
import uuid
from decimal import Decimal

class Restaurant(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    average_price = models.DecimalField(max_digits=10, decimal_places=2)
    rating = models.FloatField()
    image = models.URLField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.name

class MenuItem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='menu_items')
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name