from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from main.models import Restaurant
from review.models import Review  

class ReviewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword123')
        self.restaurant = Restaurant.objects.create(
            name='Test Restaurant',
            location='Jakarta',
            average_price=50000,
            rating=4
        )
        self.client.login(username='testuser', password='testpassword123')

    def test_add_review_ajax(self):
        response = self.client.post(reverse('add_review_ajax', args=[self.restaurant.name]), {
            'rating': 5,
            'comment': 'Makanannya luar biasa!',
            'restaurant_name': self.restaurant.name 
        })
        self.assertEqual(response.status_code, 200)  
        self.assertTrue(Review.objects.filter(user=self.user, restaurant_name=self.restaurant.name).exists()) 

    def test_edit_review(self):
        review = Review.objects.create(
            user=self.user,
            restaurant_name=self.restaurant.name, 
            rating=4,
            comment='Makanan enak!'
        )
        response = self.client.post(reverse('edit_review_ajax'), {
            'review_id': review.id,
            'rating': 5,
            'comment': 'Makanannya luar biasa!',
        })
        self.assertEqual(response.status_code, 200)
        updated_review = Review.objects.get(id=review.id)
        self.assertEqual(updated_review.rating, 5)
        self.assertEqual(updated_review.comment, 'Makanannya luar biasa!')

    def test_restaurant_review_view(self):
        review = Review.objects.create(
            user=self.user,
            restaurant_name=self.restaurant.name,
            rating=4,
            comment='Makanan enak!'
        )
        response = self.client.get(reverse('restaurant_review', args=[self.restaurant.name])) 
        self.assertEqual(response.status_code, 200)  
        self.assertContains(response, 'Makanan enak!')
        self.assertContains(response, '4/5') 

    def test_delete_review(self):
        review = Review.objects.create(
            user=self.user,
            restaurant_name=self.restaurant.name,
            rating=4,
            comment='Makanan enak!'
        )
        
        response = self.client.post(reverse('delete_review', args=[review.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Review.objects.filter(id=review.id).exists())
