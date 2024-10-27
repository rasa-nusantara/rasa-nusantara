from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from main.models import Restaurant
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.admin.views.decorators import staff_member_required
from django.forms import ModelForm

class RestaurantForm(ModelForm):
    class Meta:
        model = Restaurant
        fields = ['name', 'location', 'average_price', 'rating']

@staff_member_required(login_url='main:login')
def admin_restaurant_view(request):
    restaurants = Restaurant.objects.all()
    context = {
        'restaurants': restaurants
    }
    return render(request, 'adminview/admin_restaurant.html', context)

@staff_member_required(login_url='main:login')
def add_restaurant(request):
    if request.method == 'POST':
        form = RestaurantForm(request.POST)
        if form.is_valid():
            form.save()
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': True,
                    'message': 'Restaurant added successfully!',
                    'redirect_url': reverse('adminview:admin_restaurant')
                })
            messages.success(request, 'Restaurant added successfully!')
            return redirect('adminview:admin_restaurant')
        else:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': False,
                    'message': 'Please correct the form errors.',
                    'errors': form.errors
                })
    else:
        form = RestaurantForm()
    
    return render(request, 'adminview/add_restaurant.html', {'form': form})

@staff_member_required(login_url='main:login')
def edit_restaurant(request, uuid):
    restaurant = get_object_or_404(Restaurant, id=uuid)
    
    if request.method == 'POST':
        form = RestaurantForm(request.POST, instance=restaurant)
        if form.is_valid():
            form.save()
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': True,
                    'message': 'Restaurant updated successfully!',
                    'redirect_url': reverse('adminview:admin_restaurant')
                })
            messages.success(request, 'Restaurant updated successfully!')
            return redirect('adminview:admin_restaurant')
        else:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': False,
                    'message': 'Please correct the form errors.',
                    'errors': form.errors
                })
    else:
        form = RestaurantForm(instance=restaurant)
    
    return render(request, 'adminview/edit_restaurant.html', {
        'form': form,
        'restaurant': restaurant
    })

@staff_member_required(login_url='main:login')
def delete_restaurant(request, uuid):
    restaurant = get_object_or_404(Restaurant, id=uuid)
    restaurant.delete()
    messages.success(request, 'Restaurant deleted successfully!')
    return redirect('adminview:admin_restaurant')