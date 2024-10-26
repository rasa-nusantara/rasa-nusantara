from django.test import TestCase

# Create your tests here.
from .models import Restaurant

class RestaurantModelTest(TestCase):
    def setUp(self):
        self.restaurant = Restaurant.objects.create(
            name="Test Restaurant",
            location="Test Location",
            average_price=100.00,
            rating=4.5
        )

    def test_restaurant_creation(self):
        self.assertTrue(isinstance(self.restaurant, Restaurant))
        self.assertEqual(self.restaurant.__str__(), self.restaurant.name)
