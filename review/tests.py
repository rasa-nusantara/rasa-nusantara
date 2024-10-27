from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Review
from main.models import Restaurant

class RestaurantReviewTests(TestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.restaurant = Restaurant.objects.create(name='Mirota Bakery & Resto', location='Gondokusuman', average_price=50000, rating=4)

    def test_add_review(self):
        self.client.login(username='testuser', password='password123')

        response = self.client.post(reverse('review:add_review_ajax', kwargs={'restaurant_name': self.restaurant.name}),
                                    data={'rating': 5, 'comment': 'Makanannya enak sekali!'})

        self.assertEqual(response.status_code, 200)
        self.assertTrue(Review.objects.filter(user=self.user, restaurant_name=self.restaurant.name).exists())

    def test_edit_review(self):
        self.client.login(username='testuser', password='password123')

        review = Review.objects.create(user=self.user, restaurant_name=self.restaurant.name, rating=4, comment='Enak')

    
        response = self.client.post(reverse('review:edit_review_ajax'),
                                    data={'review_id': review.id, 'rating': 5, 'comment': 'Makanannya sangat enak!'})

        self.assertEqual(response.status_code, 200)
        review.refresh_from_db()
        self.assertEqual(review.rating, 5)
        self.assertEqual(review.comment, 'Makanannya sangat enak!')

    def test_delete_review(self):
        self.client.login(username='testuser', password='password123')

        review = Review.objects.create(user=self.user, restaurant_name=self.restaurant.name, rating=4, comment='Enak')

        response = self.client.post(reverse('review:delete_review', kwargs={'id': review.id}))

        self.assertEqual(response.status_code, 302)  # Redirect setelah penghapusan
        self.assertFalse(Review.objects.filter(id=review.id).exists())

    def test_review_display_on_restaurant_page(self):
        review = Review.objects.create(user=self.user, restaurant_name=self.restaurant.name, rating=4, comment='Makanan enak')

        response = self.client.get(reverse('review:restaurant_review', kwargs={'name': self.restaurant.name}))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Makanan enak')
        self.assertContains(response, '4/5')
        self.assertContains(response, self.user.username)
