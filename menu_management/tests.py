from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from main.models import Restaurant, MenuItem, Category
from .forms import MenuItemForm

User = get_user_model()

class MenuManagementTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_superuser(username='admin', password='password')
        self.restaurant = Restaurant.objects.create(
            name='Test Restaurant',
            location='Test Location',
            average_price=10.00,
            rating=4.5
        )
        self.category1 = Category.objects.create(name='Mie')
        self.category2 = Category.objects.create(name='Nasi')
        self.menu_item = MenuItem.objects.create(
            restaurant=self.restaurant,
            name='Indomie',
        )
        self.menu_item.categories.add(self.category1)

    def test_admin_menu_view(self):
        self.client.login(username='admin', password='password')
        response = self.client.get(reverse('adminview:admin_menu', args=[self.restaurant.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'menu_management/admin_menu.html')
        self.assertContains(response, 'Menu for Test Restaurant')

    def test_add_menu_view(self):
        self.client.login(username='admin', password='password')
        response = self.client.post(reverse('adminview:add_menu', args=[self.restaurant.id]), {
            'name': 'Nasi Goreng',
            'categories': 'Makanan, Spesial'
        })
        self.assertRedirects(response, reverse('adminview:admin_menu', args=[self.restaurant.id]))
        self.assertTrue(MenuItem.objects.filter(name='Nasi Goreng').exists())

    def test_edit_menu_view(self):
        self.client.login(username='admin', password='password')
        response = self.client.post(reverse('adminview:edit_menu', args=[self.restaurant.id, self.menu_item.id]), {
            'name': 'Indomie Goreng',
            'categories': 'Mie'
        })
        self.assertRedirects(response, reverse('adminview:admin_menu', args=[self.restaurant.id]))
        self.menu_item.refresh_from_db()
        self.assertEqual(self.menu_item.name, 'Indomie Goreng')

    def test_delete_menu_view(self):
        self.client.login(username='admin', password='password')
        response = self.client.post(reverse('adminview:delete_menu', args=[self.restaurant.id, self.menu_item.id]))
        self.assertRedirects(response, reverse('adminview:admin_menu', args=[self.restaurant.id]))
        self.assertFalse(MenuItem.objects.filter(id=self.menu_item.id).exists())

    def test_category_assignment(self):
        self.client.login(username='admin', password='password')
        response = self.client.post(reverse('adminview:add_menu', args=[self.restaurant.id]), {
            'name': 'Soto',
            'categories': 'Soto, Makanan'
        })
        new_item = MenuItem.objects.get(name='Soto')
        self.assertIn(self.category1, new_item.categories.all())
        self.assertIn(Category.objects.get(name='Soto'), new_item.categories.all())

