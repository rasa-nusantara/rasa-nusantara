from django.test import TestCase
from django.urls import reverse
from .models import Restaurant, Menu

class RestaurantTests(TestCase):

    def setUp(self):
        self.restaurant = Restaurant.objects.create(
            name='Restoran Sederhana',
            address='Jl. Malioboro No.1, Yogyakarta',
            rating='4.5',
            harga_rata_rata=50000
        )
        self.menu1 = Menu.objects.create(restaurant=self.restaurant, name='Nasi Goreng')
        self.menu2 = Menu.objects.create(restaurant=self.restaurant, name='Mie Ayam')

    def test_homepage_view(self):
        response = self.client.get(reverse('main:homepage'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main.html')

    def test_restaurant_list_view(self):
        response = self.client.get(reverse('main:restaurant_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'restaurant_list.html')
        self.assertContains(response, self.restaurant.name)
        self.assertContains(response, self.restaurant.address)

    def test_restaurant_detail_view(self):
        response = self.client.get(reverse('main:restaurant_detail', args=[self.restaurant.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'restaurant_detail.html')
        self.assertContains(response, self.restaurant.name)
        self.assertContains(response, self.menu1.name)
        self.assertContains(response, self.menu2.name)

    def test_restaurant_detail_view_404(self):
        response = self.client.get(reverse('main:restaurant_detail', args=[999]))
        self.assertEqual(response.status_code, 404)
