from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from main.models import Restaurant
from .models import Reservation
from .forms import ReservationForm
from django.utils import timezone

class ReservationTests(TestCase):
    def setUp(self):
        # Create a user
        self.user = User.objects.create_user(username='testuser', password='testpass')
        # Create a restaurant
        self.restaurant = Restaurant.objects.create(name='Test Restaurant', location='Test Location', average_price=100, rating=4.5)
        # Create a reservation
        self.reservation = Reservation.objects.create(
            user=self.user,
            restaurant=self.restaurant,
            reservation_date=timezone.now().date(),
            reservation_time=timezone.now().time(),
            number_of_people=2,
            special_request='None'
        )

    def test_create_reservation(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(reverse('reservasi:create_reservation', args=[self.restaurant.id]), {
            'reservation_date': timezone.now().date(),
            'reservation_time': timezone.now().time(),
            'number_of_people': 3,
            'special_request': 'Window seat'
        })
        self.assertEqual(response.status_code, 302)  # Check for redirect
        self.assertEqual(Reservation.objects.count(), 2)  # Check that a new reservation was created

    def test_cancel_reservation(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(reverse('reservasi:cancel_reservation', args=[self.reservation.id]))
        self.assertEqual(response.status_code, 302)  # Check for redirect
        self.assertEqual(Reservation.objects.count(), 0)  # Check that the reservation was deleted

    def test_edit_reservation(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(reverse('reservasi:edit_reservation', args=[self.reservation.id]), {
            'reservation_date': timezone.now().date(),
            'reservation_time': timezone.now().time(),
            'number_of_people': 4,
            'special_request': 'Extra napkins'
        })
        self.assertEqual(response.status_code, 200)  # Check for success response
        self.reservation.refresh_from_db()  # Refresh the reservation instance
        self.assertEqual(self.reservation.number_of_people, 4)  # Check that the number of people was updated

    def test_user_reservations_view(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('reservasi:user_reservations'))
        self.assertEqual(response.status_code, 200)  # Check for success response
        self.assertContains(response, self.reservation.restaurant.name)  # Check that the reservation is in the response

    def test_create_reservation_redirects_when_not_logged_in(self):
        response = self.client.get(reverse('reservasi:create_reservation', args=[self.restaurant.id]))
        self.assertEqual(response.status_code, 302)  # Check for redirect to login
        self.assertRedirects(response, '/login?next=/reservasi/create/' + str(self.restaurant.id) + '/')

    def test_cancel_reservation_redirects_when_not_logged_in(self):
        response = self.client.get(reverse('reservasi:cancel_reservation', args=[self.reservation.id]))
        self.assertEqual(response.status_code, 302)  # Check for redirect to login
        self.assertRedirects(response, '/login?next=/reservasi/cancel/' + str(self.reservation.id) + '/')

    def test_edit_reservation_redirects_when_not_logged_in(self):
        response = self.client.get(reverse('reservasi:edit_reservation', args=[self.reservation.id]))
        self.assertEqual(response.status_code, 302)  # Check for redirect to login
        self.assertRedirects(response, '/login?next=/reservasi/edit/' + str(self.reservation.id) + '/')
