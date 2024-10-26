from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from main.models import Restaurant  
from .models import Favorite  
from django.http import JsonResponse

@login_required
def favorite_list(request):
    favorites = Favorite.objects.filter(user=request.user)  # Ambil semua favorit milik user
    return render(request, 'favorite_list.html', {'favorites': favorites})

@login_required
def remove_favorite(request, restaurant_id):
    if request.method == 'POST':
        restaurant = get_object_or_404(Restaurant, id=restaurant_id)
        favorite = Favorite.objects.filter(user=request.user, restaurant=restaurant)
        
        if favorite.exists():
            favorite.delete()
            return JsonResponse({'success': True, 'message': 'Favorite removed successfully'})
        else:
            return JsonResponse({'success': False, 'message': 'Favorite not found'}, status=404)
    else:
        return JsonResponse({'success': False, 'message': 'Invalid request method'}, status=400)


