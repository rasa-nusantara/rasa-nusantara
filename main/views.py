from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse
from django.core import serializers
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.http import HttpResponseRedirect, JsonResponse
import datetime
from favorite.models import Favorite
from main.models import Restaurant
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from favorite.models import Favorite
from main.models import Restaurant, Category

def homepage(request):
    restaurants = Restaurant.objects.order_by('-rating')[:8]
    user_favorites = []
    if request.user.is_authenticated:
        user_favorites = Favorite.objects.filter(user=request.user).values_list('restaurant__id', flat=True)

    context = {
        'restaurants': restaurants,
        'user_favorites': user_favorites,
    }
    return render(request, 'main.html', context)

def show_json(request):
    restaurants = Restaurant.objects.all()
    restaurant_list = []
    
    for restaurant in restaurants:
        menu_items = restaurant.menu_items.all()  # Mengambil semua menu items untuk restaurant ini
        
        restaurant_data = {
            'id': str(restaurant.id),  # Convert UUID to string
            'name': restaurant.name,
            'location': restaurant.location,
            'average_price': str(restaurant.average_price),  # Convert Decimal to string
            'rating': restaurant.rating,
            'image': restaurant.image,
            'menu_items': [
                {
                    'id': str(item.id),
                    'name': item.name
                } for item in menu_items
            ]
        }
        restaurant_list.append(restaurant_data)
    
    return JsonResponse(restaurant_list, safe=False)

@login_required
def toggle_favorite(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)
    favorite, created = Favorite.objects.get_or_create(user=request.user, restaurant=restaurant)
    if not created:
        favorite.delete() 
        is_favorite = False
    else:
        is_favorite = True
    return JsonResponse({'is_favorite': is_favorite})

def restaurant(request):
    restaurants = Restaurant.objects.all()
    context = {
        'restaurants': restaurants
    }
    return render(request, 'page_restaurant.html', context)

def register(request):
    form = UserCreationForm()

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been successfully created!')
            return redirect('main:login')
    context = {'form':form}
    return render(request, 'register.html', context)

def login_user(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if user.is_staff:
                response = HttpResponseRedirect(reverse("adminview:admin_restaurant"))
            else:
                response = HttpResponseRedirect(reverse("main:homepage"))
            response.set_cookie('last_login', str(datetime.datetime.now()))
            return response
        else:
            messages.error(request, 'Username atau password salah. Coba lagi.')
    else:
        form = AuthenticationForm(request)
    context = {'form': form}
    return render(request, 'login.html', context)

def logout_user(request):
    logout(request)
    response = HttpResponseRedirect(reverse('main:homepage'))
    response.delete_cookie('last_login')
    return (response)

def product_detail(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)
    user_favorites = []
    if request.user.is_authenticated:
        user_favorites = Favorite.objects.filter(user=request.user).values_list('restaurant__id', flat=True)

    referer = request.META.get('HTTP_REFERER', '')
    
    context = {
        'restaurant': restaurant,
        'user_favorites': user_favorites,
        'referer': referer
    }
    return render(request, 'product_detail.html', context)

def restaurant_list(request):
    restaurants = Restaurant.objects.all()

    user_favorites = []
    if request.user.is_authenticated:
        user_favorites = Favorite.objects.filter(user=request.user).values_list('restaurant__id', flat=True)

    categories = Category.objects.all()

    category_id = request.GET.get('category')
    sort_option = request.GET.get('sorting')

    if category_id:
        restaurants = restaurants.filter(menu_items__categories__id=category_id).distinct()

    if sort_option == 'low_to_high':
        restaurants = restaurants.order_by('average_price')
    elif sort_option == 'high_to_low':
        restaurants = restaurants.order_by('-average_price')

    context = {
        'restaurants': restaurants,
        'categories': categories,
        'selected_category': int(category_id) if category_id else None,
        'selected_sort': sort_option,
        'user_favorites': user_favorites,
    }
    return render(request, 'page_restaurant.html', context)