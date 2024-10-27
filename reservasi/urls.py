from django.urls import path
from . import views
from uuid import UUID

app_name = 'reservasi'

urlpatterns = [
    path('create/<uuid:restaurant_id>/', views.create_reservation, name='create_reservation'),  # Updated to accept UUID
    path('cancel/<int:reservation_id>/', views.cancel_reservation, name='cancel_reservation'),
    path('edit/<int:reservation_id>/', views.edit_reservation, name='edit_reservation'),
    path('user_reservations/', views.user_reservations, name='user_reservations'),
]
