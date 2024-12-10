from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from favorite.models import Favorite
from decimal import Decimal
from django.conf import settings
from django.core.management import call_command
from io import StringIO
import os
import json
from django.core.management.base import CommandError
from main.models import Restaurant, Category
from decimal import Decimal

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


class AddCategoriesCommandTest(TestCase):
    def setUp(self):
        Category.objects.all().delete()

    def test_add_categories(self):
        out = StringIO()
        call_command('add_categories', stdout=out)
        
        expected_categories = [
            "Gudeg", "Oseng", "Bakpia", "Sate", "Sego Gurih",
            "Wedang", "Lontong", "Rujak Cingur", "Mangut Lele", "Ayam", "Lainnya"
        ]
        
        for category_name in expected_categories:
            self.assertTrue(Category.objects.filter(name=category_name).exists())
        
        for category_name in expected_categories:
            self.assertIn(f"Category '{category_name}' created.", out.getvalue())
        
        self.assertIn("Categories added successfully!", out.getvalue())

    def test_add_categories_when_already_exists(self):

        existing_categories = ["Gudeg", "Bakpia", "Lontong"]
        for category_name in existing_categories:
            Category.objects.create(name=category_name)

        out = StringIO()
        call_command('add_categories', stdout=out)

        expected_categories = [
            "Gudeg", "Oseng", "Bakpia", "Sate", "Sego Gurih",
            "Wedang", "Lontong", "Rujak Cingur", "Mangut Lele", "Ayam", "Lainnya"
        ]

        for category_name in expected_categories:
            self.assertTrue(Category.objects.filter(name=category_name).exists())

        for category_name in existing_categories:
            self.assertIn(f"Category '{category_name}' already exists.", out.getvalue())

        new_categories = set(expected_categories) - set(existing_categories)
        for category_name in new_categories:
            self.assertIn(f"Category '{category_name}' created.", out.getvalue())
        
        self.assertIn("Categories added successfully!", out.getvalue())

class LoadDataCommandTests(TestCase):
    def setUp(self):
        self.test_file_path = os.path.join(os.path.dirname(__file__), 'test_data.json')
        with open(self.test_file_path, 'w', encoding='utf-8') as f:
            json.dump([
                {
                    "Nama Restoran": "Test Restaurant",
                    "Lokasi Restoran": "Test Location",
                    "Harga Rata-Rata Makanan di Toko (Rp)": "100000",
                    "Rating Toko": "4.5",
                    "Foto": "https://example.com/image.jpg",
                    "Variasi Makanan": "Nasi Goreng, Mie Goreng",
                    "Kategori": "Indonesian, Asian"
                }
            ], f)

    def tearDown(self):
        if os.path.exists(self.test_file_path):
            os.remove(self.test_file_path)

    def test_load_valid_data(self):
        out = StringIO()
        call_command('load_data', file=self.test_file_path, stdout=out)
        self.assertIn("Successfully processed Restaurant: Test Restaurant", out.getvalue())

    def test_load_nonexistent_file(self):
        with self.assertRaises(CommandError):
            call_command('load_data', file="nonexistent.json")

    def test_invalid_json(self):
        invalid_file_path = os.path.join(os.path.dirname(__file__), 'invalid_data.json')
        with open(invalid_file_path, 'w', encoding='utf-8') as f:
            f.write("{ invalid json }")
        with self.assertRaises(CommandError):
            call_command('load_data', file=invalid_file_path)
        os.remove(invalid_file_path)

