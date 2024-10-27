from django.urls import path
from .views import admin_restaurant_view, edit_restaurant, delete_restaurant, add_restaurant, admin_menu_view, add_menu, edit_menu, delete_menu

app_name = 'adminview'

urlpatterns = [
    path('', admin_restaurant_view, name='admin_restaurant'),
    path('edit/<str:uuid>/', edit_restaurant, name='edit_restaurant'),  # Changed from uuid:uuid to str:uuid
    path('delete/<str:uuid>/', delete_restaurant, name='delete_restaurant'),  # Changed from uuid:uuid to str:uuid
    path('add/', add_restaurant, name='add_restaurant'),
    path('admin_menu/<uuid:restaurant_id>/', admin_menu_view, name='admin_menu'),
    path('admin_menu/add/<uuid:restaurant_id>/', add_menu, name='add_menu'),
    path('admin_menu/edit/<uuid:restaurant_id>/<uuid:id>/', edit_menu, name='edit_menu'),
    path('admin_menu/delete/<uuid:restaurant_id>/<uuid:id>/', delete_menu, name='delete_menu'),
]
