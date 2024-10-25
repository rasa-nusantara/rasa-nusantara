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
from main.models import Restaurant

def homepage(request, login_failed=False):
    restaurants = Restaurant.objects.order_by('-rating')[:4]
    user_favorites = []
    if request.user.is_authenticated:
        user_favorites = Favorite.objects.filter(user=request.user).values_list('restaurant__id', flat=True)

    context = {
        'restaurants': restaurants,
        'user_favorites': user_favorites, 
        'login_failed': login_failed
    }
    return render(request, 'main.html', context)

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
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('main:homepage')  # Redirect ke homepage jika login sukses
        else:
            messages.error(request, "Username atau password yang Anda masukkan salah.")
            return homepage(request, login_failed=True)  # Kirimkan flag login_failed ke homepage view
    return homepage(request, login_failed=False)

def logout_user(request):
    logout(request)
    response = HttpResponseRedirect(reverse('main:homepage'))
    response.delete_cookie('last_login')
    return (response)

def product_detail(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)
    return render(request, 'product_detail.html', {'restaurant': restaurant})