from django.shortcuts import redirect, get_object_or_404
from .models import Favorite
from adminview.models import Restaurant
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def toggle_favorite(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)
    
    favorite, created = Favorite.objects.get_or_create(user=request.user, restaurant=restaurant)
    
    if not created:
        favorite.delete()
        action = 'removed'
    else:
        action = 'added'
    
    return redirect('restaurant_detail', restaurant_id=restaurant.id)

@login_required
def favorite_list(request):
    favorites = request.user.favorites.all()
    return render(request, 'favorites/favorite_list.html', {'favorites': favorites})