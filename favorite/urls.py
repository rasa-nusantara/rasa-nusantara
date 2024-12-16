from django.urls import path
from favorite.views import remove_favorite, favorite_list, toggle_favorite, favorite_list_json

app_name = 'favorite'

urlpatterns = [
    path('list/', favorite_list, name='favorite_list'),  
    path('favorite/remove/<uuid:restaurant_id>/', remove_favorite, name='remove_favorite'),
    path('toggle-favorite/', toggle_favorite, name='toggle_favorite'),
    path('favorite/json', favorite_list_json, name='favorite_list_json'),
]
