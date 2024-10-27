from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from main.models import Restaurant
import json

class AdminRestaurantViewTests(TestCase):
    def setUp(self):
        # Create a superuser
        User = get_user_model()
        self.admin_user = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='adminpass123'
        )
        
        # Create a regular user
        self.regular_user = User.objects.create_user(
            username='user',
            email='user@example.com',
            password='userpass123'
        )
        
        # Create a test restaurant
        self.restaurant = Restaurant.objects.create(
            name='Test Restaurant',
            location='Test Location',
            average_price=10.99,
            rating=4.5
        )
        
        self.client = Client()

    def test_admin_restaurant_view_template(self):
        """Test the admin restaurant view template rendering"""
        self.client.login(username='admin', password='adminpass123')
        response = self.client.get(reverse('adminview:admin_restaurant'))
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'adminview/admin_restaurant.html')
        self.assertIn('restaurants', response.context)
        self.assertQuerysetEqual(
            response.context['restaurants'],
            Restaurant.objects.all(),
            transform=lambda x: x
        )

    def test_add_restaurant_get(self):
        """Test GET request for add restaurant page"""
        self.client.login(username='admin', password='adminpass123')
        response = self.client.get(reverse('adminview:add_restaurant'))
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'adminview/add_restaurant.html')
        self.assertIn('form', response.context)

    def test_add_restaurant_post_normal(self):
        """Test normal POST request for adding restaurant"""
        self.client.login(username='admin', password='adminpass123')
        data = {
            'name': 'New Restaurant',
            'location': 'New Location',
            'average_price': 15.99,
            'rating': 4.0
        }
        response = self.client.post(reverse('adminview:add_restaurant'), data)
        
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('adminview:admin_restaurant'))
        self.assertTrue(Restaurant.objects.filter(name='New Restaurant').exists())

    def test_add_restaurant_post_ajax(self):
        """Test AJAX POST request for adding restaurant"""
        self.client.login(username='admin', password='adminpass123')
        data = {
            'name': 'Ajax Restaurant',
            'location': 'Ajax Location',
            'average_price': 25.99,
            'rating': 4.8
        }
        response = self.client.post(
            reverse('adminview:add_restaurant'),
            data=data,
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.content)
        self.assertTrue(response_data['success'])
        self.assertEqual(response_data['message'], 'Restaurant added successfully!')
        self.assertTrue(Restaurant.objects.filter(name='Ajax Restaurant').exists())

    def test_add_restaurant_invalid_data_ajax(self):
        """Test AJAX POST request with invalid data"""
        self.client.login(username='admin', password='adminpass123')
        data = {
            'name': '',  # Invalid: empty name
            'location': 'Test Location',
            'average_price': 'invalid',  # Invalid: not a number
            'rating': 6  # Invalid: rating > 5
        }
        response = self.client.post(
            reverse('adminview:add_restaurant'),
            data=data,
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.content)
        self.assertFalse(response_data['success'])
        self.assertIn('errors', response_data)

    def test_edit_restaurant_get(self):
        """Test GET request for edit restaurant page"""
        self.client.login(username='admin', password='adminpass123')
        response = self.client.get(
            reverse('adminview:edit_restaurant', kwargs={'uuid': str(self.restaurant.id)})
        )
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'adminview/edit_restaurant.html')
        self.assertIn('form', response.context)
        self.assertIn('restaurant', response.context)

    def test_edit_restaurant_post_normal(self):
        """Test normal POST request for editing restaurant"""
        self.client.login(username='admin', password='adminpass123')
        data = {
            'name': 'Updated Restaurant',
            'location': 'Updated Location',
            'average_price': 20.99,
            'rating': 4.8
        }
        response = self.client.post(
            reverse('adminview:edit_restaurant', kwargs={'uuid': str(self.restaurant.id)}),
            data=data
        )
        
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('adminview:admin_restaurant'))
        updated_restaurant = Restaurant.objects.get(id=self.restaurant.id)
        self.assertEqual(updated_restaurant.name, 'Updated Restaurant')

    def test_edit_restaurant_post_ajax(self):
        """Test AJAX POST request for editing restaurant"""
        self.client.login(username='admin', password='adminpass123')
        data = {
            'name': 'Ajax Updated Restaurant',
            'location': 'Ajax Updated Location',
            'average_price': 30.99,
            'rating': 4.9
        }
        response = self.client.post(
            reverse('adminview:edit_restaurant', kwargs={'uuid': str(self.restaurant.id)}),
            data=data,
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.content)
        self.assertTrue(response_data['success'])
        updated_restaurant = Restaurant.objects.get(id=self.restaurant.id)
        self.assertEqual(updated_restaurant.name, 'Ajax Updated Restaurant')

    def test_edit_restaurant_invalid_data_ajax(self):
        """Test AJAX POST request with invalid data for editing"""
        self.client.login(username='admin', password='adminpass123')
        data = {
            'name': '',  # Invalid: empty name
            'location': 'Test Location',
            'average_price': 'invalid',  # Invalid: not a number
            'rating': 6  # Invalid: rating > 5
        }
        response = self.client.post(
            reverse('adminview:edit_restaurant', kwargs={'uuid': str(self.restaurant.id)}),
            data=data,
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.content)
        self.assertFalse(response_data['success'])
        self.assertIn('errors', response_data)

    def test_delete_restaurant_post(self):
        """Test POST request for deleting restaurant"""
        self.client.login(username='admin', password='adminpass123')
        response = self.client.post(
            reverse('adminview:delete_restaurant', kwargs={'uuid': str(self.restaurant.id)})
        )
        
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('adminview:admin_restaurant'))
        self.assertFalse(Restaurant.objects.filter(id=self.restaurant.id).exists())

    def test_invalid_restaurant_uuid(self):
        """Test accessing non-existent restaurant"""
        self.client.login(username='admin', password='adminpass123')
        
        # Try to edit non-existent restaurant
        response = self.client.get(
            reverse('adminview:edit_restaurant', kwargs={'uuid': '12345678-1234-5678-1234-567812345678'})
        )
        self.assertEqual(response.status_code, 404)
        
        # Try to delete non-existent restaurant
        response = self.client.post(
            reverse('adminview:delete_restaurant', kwargs={'uuid': '12345678-1234-5678-1234-567812345678'})
        )
        self.assertEqual(response.status_code, 404)

    def test_unauthorized_access(self):
        """Test access control"""
        # Try accessing without login
        response = self.client.get(reverse('adminview:admin_restaurant'))
        self.assertRedirects(response, '/login/?next=' + reverse('adminview:admin_restaurant'))
        
        # Try accessing with regular user
        self.client.login(username='user', password='userpass123')
        response = self.client.get(reverse('adminview:admin_restaurant'))
        self.assertEqual(response.status_code, 302)  # Should redirect to login