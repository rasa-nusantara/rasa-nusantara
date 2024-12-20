from django.urls import path
from . import views
from uuid import UUID

app_name = 'reservasi'

urlpatterns = [
    path('create/<uuid:restaurant_id>/', views.create_reservation, name='create_reservation'),  # Updated to accept UUID
    path('cancel/<int:reservation_id>/', views.cancel_reservation, name='cancel_reservation'),
    path('edit/<int:reservation_id>/', views.edit_reservation, name='edit_reservation'),
    path('user_reservations/', views.user_reservations, name='user_reservations'),
    path('json/', views.show_json, name='show_json'),
    path('create_reservation_flutter/<uuid:restaurant_id>/', views.create_reservation_flutter, name='create_reservation_flutter'),
    path('cancel_flutter/<int:reservation_id>/', views.cancel_reservation_flutter, name='cancel_reservation_flutter'),
    path('edit_flutter/<int:reservation_id>/', views.edit_reservation_flutter, name='edit_reservation_flutter'),
]
