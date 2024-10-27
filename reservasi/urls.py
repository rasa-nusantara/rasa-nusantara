from django.urls import path
from . import views

app_name = 'reservasi'

urlpatterns = [
    path('', views.index, name='index'),
    path('new/', views.create_reservation, name='create_reservation'),
]
