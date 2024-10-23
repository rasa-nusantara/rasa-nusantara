from django.shortcuts import render, redirect, get_object_or_404
from .models import Restaurant, Menu
from .forms import RestaurantForm, MenuForm
from django.contrib.auth.decorators import user_passes_test

# Custom decorator untuk memastikan hanya admin (staff) yang bisa mengakses
def is_admin(user):
    return user.is_staff

# Halaman dashboard admin untuk melihat dan menambah restoran
@user_passes_test(is_admin)
def admin_dashboard(request):
    restaurants = Restaurant.objects.all()
    return render(request, 'admin_app/admin_dashboard.html', {'restaurants': restaurants})

# Menambahkan restoran baru
@user_passes_test(is_admin)
def add_restaurant(request):
    if request.method == 'POST':
        form = RestaurantForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_app:admin_dashboard')
    else:
        form = RestaurantForm()
    return render(request, 'admin_app/add_restaurant.html', {'form': form})

# Menambahkan menu baru untuk restoran
@user_passes_test(is_admin)
def add_menu(request):
    if request.method == 'POST':
        form = MenuForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_app:admin_dashboard')
    else:
        form = MenuForm()
    return render(request, 'admin_app/add_menu.html', {'form': form})

# View untuk user melihat daftar restoran dan menu
def restaurant_list(request):
    restaurants = Restaurant.objects.all()
    return render(request, 'admin_app/restaurant_list.html', {'restaurants': restaurants})

def restaurant_detail(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)
    menus = restaurant.menus.all()
    return render(request, 'admin_app/restaurant_detail.html', {'restaurant': restaurant, 'menus': menus})
