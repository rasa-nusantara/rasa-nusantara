# adminview/urls.py
from django.urls import path, register_converter
from uuid import UUID



class UUIDConverter:
    regex = '[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}'

    def to_python(self, value):
        return UUID(value)

    def to_url(self, value):
        return str(value)

# Register the converter
register_converter(UUIDConverter, 'uuid')

from .views import (
    admin_restaurant_view,
    edit_restaurant,
    delete_restaurant,
    add_restaurant,
    admin_menu_view,  # imported from menu_management
    add_menu,         # imported from menu_management
    edit_menu,        # imported from menu_management
    delete_menu       # imported from menu_management
)

app_name = 'adminview'

urlpatterns = [
    path('', admin_restaurant_view, name='admin_restaurant'),
    path('edit/<uuid:id>/', edit_restaurant, name='edit_restaurant'),
    path('delete/<uuid:id>/', delete_restaurant, name='delete_restaurant'),
    path('add/', add_restaurant, name='add_restaurant'),
    path('admin_menu/<uuid:restaurant_id>/', admin_menu_view, name='admin_menu'),
    path('admin_menu/add/<uuid:restaurant_id>/', add_menu, name='add_menu'),
    path('admin_menu/edit/<uuid:restaurant_id>/<uuid:id>/', edit_menu, name='edit_menu'),
    path('admin_menu/delete/<uuid:restaurant_id>/<uuid:id>/', delete_menu, name='delete_menu'),
]
