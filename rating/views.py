# rating/views.py
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from main.models import Restaurant
from .models import Rating
from django.contrib.auth.decorators import login_required

@login_required
def rate_restaurant(request, restaurant_id):
    if request.method == 'POST':
        restaurant = get_object_or_404(Restaurant, id=restaurant_id)
        score = int(request.POST.get('score'))

        rating, created = Rating.objects.update_or_create(
            restaurant=restaurant, user=request.user, defaults={'score': score}
        )

        restaurant.update_average_rating()

        return JsonResponse({'success': True, 'new_average': restaurant.rating})
    return JsonResponse({'success': False}, status=400)
