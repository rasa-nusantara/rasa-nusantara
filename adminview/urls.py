from django.urls import path
from .views import admin_restaurant_view, edit_restaurant, delete_restaurant, add_restaurant

app_name = 'adminview'

urlpatterns = [
    path('', admin_restaurant_view, name='admin_restaurant'),
    path('edit/<str:uuid>/', edit_restaurant, name='edit_restaurant'),  # Changed from uuid:uuid to str:uuid
    path('delete/<str:uuid>/', delete_restaurant, name='delete_restaurant'),  # Changed from uuid:uuid to str:uuid
    path('add/', add_restaurant, name='add_restaurant'),
]