from django.urls import path
from . import views

urlpatterns = [
    path('restaurant-list/', views.restaurant_list, name='restaurant_list'),
    path('restaurant-review/<str:name>/', views.restaurant_review, name='restaurant_review'),
    # path('restaurant-review/add/<str:restaurant_name>/', views.add_review, name='add_review'),
    path('restaurant-review/edit/<int:id>/', views.edit_review, name='edit_review'),
    path('restaurant-review/delete/<int:id>/', views.delete_review, name='delete_review'),
    path('restaurant/<str:restaurant_name>/add_review_ajax/', views.add_review_ajax, name='add_review_ajax'),
    path('edit_review_ajax/', views.edit_review_ajax, name='edit_review_ajax'),
    
    
    
]