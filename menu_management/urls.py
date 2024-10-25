from django.urls import path
from . import views

app_name = 'menu_management'

urlpatterns = [
    path('admin_menu/<int:restaurant_id>/', views.admin_menu_view, name='admin_menu'),
    path('add/<int:restaurant_id>/', views.add_menu, name='add_menu'),
    path('edit/<int:restaurant_id>/<int:id>/', views.edit_menu, name='edit_menu'),
    path('delete/<int:restaurant_id>/<int:id>/', views.delete_menu, name='delete_menu'),
]
