from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from main.models import Restaurant  
from .models import Favorite  
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.core.serializers import serialize
import json

@csrf_exempt
@login_required
def favorite_list(request):
    favorites = Favorite.objects.filter(user=request.user)  
    return render(request, 'favorite_list.html', {'favorites': favorites})

@csrf_exempt
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

@csrf_exempt
@login_required
def toggle_favorite(request):
    if request.method == 'POST':
        print("Request Received!")  # Log untuk memastikan request masuk
        print(f"Body: {request.body}")  # Log body request untuk debug
        try:
            data = json.loads(request.body)
            restaurant_id = data.get('restaurant_id')
            print(f"Restaurant ID: {restaurant_id}")  # Log ID yang diterima

            if not restaurant_id:
                return JsonResponse({'success': False, 'message': 'Restaurant ID is missing'}, status=400)

            restaurant = get_object_or_404(Restaurant, id=restaurant_id)
            favorite = Favorite.objects.filter(user=request.user, restaurant=restaurant)

            if favorite.exists():
                favorite.delete()
                return JsonResponse({'success': True, 'message': 'Favorite removed', 'status': 'unfavorited'})
            else:
                Favorite.objects.create(user=request.user, restaurant=restaurant)
                return JsonResponse({'success': True, 'message': 'Favorite added', 'status': 'favorited'})

        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'message': 'Invalid JSON'}, status=400)
    else:
        return JsonResponse({'success': False, 'message': 'Invalid request method'}, status=400)

@csrf_exempt
@login_required
def favorite_list_json(request):
    favorites = Favorite.objects.filter(user=request.user).select_related('restaurant')
    data = [
        {
            "id": favorite.restaurant.id,
            "name": favorite.restaurant.name,
            "location": favorite.restaurant.location,
            "image": favorite.restaurant.image if favorite.restaurant.image else "",
            "rating": favorite.restaurant.rating,
        }
        for favorite in favorites
    ]
    return JsonResponse(data, safe=False)
