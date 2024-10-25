from django.urls import path
from adminview.views import admin_restaurant_view, edit_restaurant, delete_restaurant, add_restaurant

app_name = 'adminview'

urlpatterns = [
    path('', admin_restaurant_view, name='admin_restaurant'),
    path('edit/<int:id>/', edit_restaurant, name='edit_restaurant'),
    path('delete/<int:id>/', delete_restaurant, name='delete_restaurant'),
    path('add/', add_restaurant, name='add_restaurant'),
]