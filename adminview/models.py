from django.db import models

class Restaurant(models.Model):
    name = models.CharField(max_length=255)
    address = models.TextField()
    rating = models.DecimalField(max_digits=2, decimal_places=1)
    harga_rata_rata = models.IntegerField()

    def __str__(self):
        return self.name

class Menu(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='menus')
    name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name} - {self.restaurant.name}"
