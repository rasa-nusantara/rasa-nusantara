# favorite/tests.py
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from main.models import Restaurant
from .models import Favorite

class FavoriteViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.restaurant = Restaurant.objects.create(
            name='Test Restaurant',
            location='Test Location',
            average_price=100,
            rating=4.5
        )
        self.client.login(username='testuser', password='password123')

    def test_add_favorite(self):
        # Tambah favorit dan periksa apakah tersimpan di database
        Favorite.objects.create(user=self.user, restaurant=self.restaurant)
        url = reverse('favorite:favorite_list')
        
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Restaurant')
        self.assertTrue(Favorite.objects.filter(user=self.user, restaurant=self.restaurant).exists())

    def test_remove_favorite(self):
        # Menambahkan restoran ke favorit sebelum dihapus
        Favorite.objects.create(user=self.user, restaurant=self.restaurant)
        url = reverse('favorite:remove_favorite', args=[self.restaurant.id])
        
        # Kirim permintaan POST untuk menghapus dan cek apakah berhasil
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)  # Redirect setelah penghapusan
        self.assertFalse(Favorite.objects.filter(user=self.user, restaurant=self.restaurant).exists())

    def test_view_favorite_list(self):
        # Tambahkan restoran ke daftar favorit
        Favorite.objects.create(user=self.user, restaurant=self.restaurant)
        url = reverse('favorite:favorite_list')
        
        # Memeriksa apakah restoran tampil di daftar favorit
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Restaurant')
