from django.shortcuts import render, get_object_or_404, redirect, reverse
from .models import Restaurant
from django.contrib.admin.views.decorators import staff_member_required
from .forms import RestaurantForm, MenuFormSet
from django.http import HttpResponse
from django.core import serializers
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.http import HttpResponseRedirect
import datetime

def homepage(request):
    restaurants_entries = Restaurant.objects.all()
    context = {'restaurants_entries' : restaurants_entries,
               }
    return render(request, 'main.html', context)

def restaurant_list(request):
    restaurants = Restaurant.objects.all()
    return render(request, 'restaurant_list.html', {'restaurants': restaurants})

def restaurant_detail(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)
    menus = restaurant.menus.all()
    return render(request, 'restaurant_detail.html', {'restaurant': restaurant, 'menus': menus})

@staff_member_required
def add_restaurant(request):
    if request.method == 'POST':
        restaurant_form = RestaurantForm(request.POST)
        menu_formset = MenuFormSet(request.POST)
        
        
        if restaurant_form.is_valid() and menu_formset.is_valid():
            # Simpan restoran
            restaurant = restaurant_form.save()

            # Simpan menu yang terkait dengan restoran
            menu_formset.instance = restaurant  # Tetapkan instance restoran
            menu_formset.save()
            
            # Redirect ke halaman daftar restoran setelah berhasil menyimpan
            return redirect('main:restaurant_list')
    else:
        # Jika GET request, tampilkan form kosong
        restaurant_form = RestaurantForm()
        menu_formset = MenuFormSet()

    return render(request, 'add_restaurant.html', {
        'restaurant_form': restaurant_form,
        'menu_formset': menu_formset,
    })

def show_xml(request):
    data = Restaurant.objects.all()
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

def show_json(request):
    data = Restaurant.objects.all()
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

def show_xml_by_id(request, id):
    data = Restaurant.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

def show_json_by_id(request, id):
    data = Restaurant.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

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
        response = HttpResponseRedirect(reverse("main:homepage"))
        response.set_cookie('last_login', str(datetime.datetime.now()))
        return response

   else:
      form = AuthenticationForm(request)
   context = {'form': form}
   return render(request, 'login.html', context)

def logout_user(request):
    logout(request)
    response = HttpResponseRedirect(reverse('main:login'))
    response.delete_cookie('last_login')
    return response