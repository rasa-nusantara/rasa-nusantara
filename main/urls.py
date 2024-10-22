from django.urls import path
from main.views import restaurant_detail, restaurant_list, homepage,add_restaurant, register, login_user, logout_user
from main.views import show_xml, show_json, show_xml_by_id, show_json_by_id

app_name = 'main'

urlpatterns = [
    path('', homepage, name='homepage'),
    path('restaurants/', restaurant_list, name='restaurant_list'),
    path('restaurants/<int:restaurant_id>/', restaurant_detail, name='restaurant_detail'),
    path('restaurants/add/', add_restaurant, name='add_restaurant'),
    path('xml/', show_xml, name='show_xml'),  
    path('json/', show_json, name='show_json'),
    path('xml/<str:id>/', show_xml_by_id, name='show_xml_by_id'),   
    path('json/<str:id>/', show_json_by_id, name='show_json_by_id'),
    path('register/', register, name='register'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
]