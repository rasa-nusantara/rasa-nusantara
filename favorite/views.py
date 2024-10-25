from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from main.models import Restaurant  # Import the Restaurant model from the main app
from .models import Favorite  # Assuming Favorite is defined in the favorite app

@login_required
def favorite_list(request):
    favorites = Favorite.objects.filter(user=request.user)
    return render(request, 'favorite_list.html', {'favorites': favorites})

@login_required
def remove_favorite(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)
    favorite = Favorite.objects.filter(user=request.user, restaurant=restaurant)
    if favorite.exists():
        favorite.delete()
    return redirect('favorite:favorite_list')
