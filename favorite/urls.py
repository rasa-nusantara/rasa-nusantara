from django.urls import path
from . import views

app_name = 'favorites'

urlpatterns = [
    path('toggle/<int:restaurant_id>/', views.toggle_favorite, name='toggle_favorite'),
    path('list/', views.favorite_list, name='favorite_list'),

]
