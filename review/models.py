from django.db import models

# Create your models here.
class Restaurant(models.Model):
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    average_price = models.DecimalField(max_digits=10, decimal_places=2)
    rating = models.FloatField()

    def __str__(self):
        return self.name

class MenuItem(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='menu_items')
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
