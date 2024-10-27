from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from main.models import Restaurant, Category
from favorite.models import Favorite
from decimal import Decimal
from django.conf import settings

class MainAppTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.category = Category.objects.create(name="Gudeg")

        self.restaurant = Restaurant.objects.create(
            name="Gudeg Mercon Bu Tinah",
            location="Jalan Malioboro",
            average_price=Decimal("50000.00"),
            rating=4.5,
            image="https://example.com/image.jpg"
        )
        
        self.restaurant.menu_items.create(name="Gudeg Spesial")
        self.restaurant.menu_items.first().categories.add(self.category)

    def test_homepage_view(self):
        response = self.client.get(reverse('main:homepage'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main.html')
        self.assertContains(response, "Restoran Populer")

    def test_register_view(self):
        response = self.client.post(reverse('main:register'), {
            'username': 'newuser',
            'password1': 'Str0ngP@ssword!',
            'password2': 'Str0ngP@ssword!'
        })
        
        if response.status_code == 200:
            print(response.context['form'].errors)

        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='newuser').exists())


    def test_login_view(self):
        response = self.client.post(reverse('main:login'), {
            'username': 'testuser',
            'password': 'testpass'
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('main:homepage'))

    def test_logout_view(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('main:logout'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('main:homepage'))

    def test_product_detail_view(self):
        url = reverse('main:product_detail', args=[self.restaurant.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'product_detail.html')
        self.assertContains(response, self.restaurant.name)

    def test_toggle_favorite(self):
        self.client.login(username='testuser', password='testpass')

        url = reverse('main:toggle_favorite', args=[self.restaurant.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Favorite.objects.filter(user=self.user, restaurant=self.restaurant).exists())

        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Favorite.objects.filter(user=self.user, restaurant=self.restaurant).exists())

    def test_restaurant_list_view(self):
        response = self.client.get(reverse('main:restaurant'), {
            'category': self.category.id,
            'sorting': 'low_to_high'
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'page_restaurant.html')
        self.assertContains(response, self.restaurant.name)

def test_anonymous_user_cannot_access_toggle_favorite(self):
    url = reverse('main:toggle_favorite', args=[self.restaurant.id])
    response = self.client.post(url)
    self.assertRedirects(response, f"{settings.LOGIN_URL}?next={url}")

