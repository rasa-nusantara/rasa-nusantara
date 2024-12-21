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
