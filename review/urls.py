from django.urls import path
from . import views
from review.views import show_json, create_review_flutter, get_restaurant_reviews, get_username, delete_review_flutter,edit_review_flutter

urlpatterns = [
    path('restaurant-review/<str:name>/', views.restaurant_review, name='restaurant_review'),
    path('restaurant-review/edit/<int:id>/', views.edit_review, name='edit_review'),
    path('restaurant-review/delete/<int:id>/', views.delete_review, name='delete_review'),
    path('restaurant/<str:restaurant_name>/add_review_ajax/', views.add_review_ajax, name='add_review_ajax'),
    path('edit_review_ajax/', views.edit_review_ajax, name='edit_review_ajax'),
    path('create-review-flutter/', views.create_review_flutter, name='create_review_flutter'),
    path('get-restaurant-reviews/<str:restaurant_name>/', views.get_restaurant_reviews, name='get_restaurant_reviews'),
    path('json/', show_json, name='show_json'),
    path('get_username/', get_username, name='get_username'),
    path('delete-review-flutter/<int:review_id>/', delete_review_flutter, name='delete_review_flutter'),
    path('edit-review-flutter/<int:review_id>/', edit_review_flutter, name='edit_review_flutter'),
    
]
