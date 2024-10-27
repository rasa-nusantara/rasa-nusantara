# favorite/tests.py
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from main.models import Restaurant
from .models import Favorite
from django.http import JsonResponse

class FavoriteViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.restaurant = Restaurant.objects.create(
            name='Test Restaurant',
            location='Test Location',
            average_price=100,
            rating=4.5
        )

    def test_favorite_list_view_authenticated(self):
        """Test if logged-in users can view the favorite list."""
        # Log the user in
        self.client.login(username='testuser', password='password123')
        
        # Add a restaurant to favorites
        Favorite.objects.create(user=self.user, restaurant=self.restaurant)
        
        # Test the favorite list view
        url = reverse('favorite:favorite_list')
        response = self.client.get(url)
        
        # Assert response status code and content
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Restaurant')
        self.assertContains(response, '(1 Restoran)')  # Checks if favorite count is displayed correctly

    def test_favorite_list_view_unauthenticated(self):
        """Test if unauthenticated users are redirected to the login page when accessing the favorite list."""
        url = reverse('favorite:favorite_list')
        response = self.client.get(url)
        
        # Assert redirect to login page
        self.assertRedirects(response, f"{reverse('main:login')}?next={url}")

    def test_add_favorite(self):
        """Test adding a restaurant to the user's favorites."""
        # Log the user in
        self.client.login(username='testuser', password='password123')
        
        # Add favorite
        Favorite.objects.create(user=self.user, restaurant=self.restaurant)
        
        # Test if the favorite exists in the database
        self.assertTrue(Favorite.objects.filter(user=self.user, restaurant=self.restaurant).exists())

    def test_remove_favorite(self):
        self.client.login(username='testuser', password='password123')
        
        Favorite.objects.create(user=self.user, restaurant=self.restaurant)
        
        url = reverse('favorite:remove_favorite', args=[self.restaurant.id])
        response = self.client.post(url, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get('success'), True)
        self.assertFalse(Favorite.objects.filter(user=self.user, restaurant=self.restaurant).exists())

    def test_remove_favorite_not_exists(self):
        self.client.login(username='testuser', password='password123')
        
        url = reverse('favorite:remove_favorite', args=[self.restaurant.id])
        response = self.client.post(url, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json().get('success'), False)
        self.assertEqual(response.json().get('message'), 'Favorite not found')
