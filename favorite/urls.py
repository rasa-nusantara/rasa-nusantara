from django.urls import path
from favorite.views import remove_favorite, favorite_list

app_name = 'favorite'

urlpatterns = [
    path('list/', favorite_list, name='favorite_list'),  # To list the favorite restaurants
path('favorite/remove/<uuid:restaurant_id>/', remove_favorite, name='remove_favorite'),]