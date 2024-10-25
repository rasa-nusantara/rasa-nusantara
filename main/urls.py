from django.urls import path
from main.views import homepage, login_user, register, logout_user, restaurant

app_name = 'main'

urlpatterns = [
    path('', homepage, name='homepage'),
    path('login', login_user, name='login'),
    path('register', register, name='register'),
    path('logout/', logout_user, name='logout'),
    path('restaurant',restaurant,name='restaurant'),
]
