# menu_management/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from main.models import Restaurant, MenuItem
from .models import MenuItem
from django.forms import ModelForm
from main.models import Restaurant, MenuItem, Category 

class MenuItemForm(ModelForm):
    class Meta:
        model = MenuItem
        fields = ['name', 'categories']

def admin_menu_view(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)  # Ensure it uses UUID
    menu_items = restaurant.menu_items.all()  # Get the menu items for the restaurant
    categories = Category.objects.all()  # Fetch all categories for use in templates
    context = {
        'restaurant': restaurant,
        'menu_items': menu_items,
        'categories': categories,  # Pass categories to the template
    }
    return render(request, 'menu_management/admin_menu.html', context)

@user_passes_test(lambda u: u.is_staff, login_url='main:login')
def add_menu(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)
    if request.method == 'POST':
        form = MenuItemForm(request.POST)
        if form.is_valid():
            menu_item = form.save(commit=False)
            menu_item.restaurant = restaurant  # Associate with the restaurant
            menu_item.save()
            messages.success(request, 'Menu item added successfully!')
            return redirect('adminview:admin_menu', restaurant_id=restaurant.id)
    else:
        form = MenuItemForm()
    return render(request, 'menu_management/add_menu.html', {'form': form, 'restaurant': restaurant})

@user_passes_test(lambda u: u.is_staff, login_url='main:login')
def edit_menu(request, restaurant_id, id):
    menu_item = get_object_or_404(MenuItem, id=id, restaurant__id=restaurant_id)
    if request.method == 'POST':
        form = MenuItemForm(request.POST, instance=menu_item)
        if form.is_valid():
            form.save()
            messages.success(request, 'Menu item updated successfully!')
            return redirect('adminview:admin_menu', restaurant_id=restaurant_id)
    else:
        form = MenuItemForm(instance=menu_item)
    return render(request, 'menu_management/edit_menu.html', {'form': form, 'restaurant': menu_item.restaurant})

@user_passes_test(lambda u: u.is_staff, login_url='main:login')
def delete_menu(request, restaurant_id, id):
    menu_item = get_object_or_404(MenuItem, id=id, restaurant__id=restaurant_id)
    menu_item.delete()
    messages.success(request, 'Menu item deleted successfully!')
    return redirect('adminview:admin_menu', restaurant_id=restaurant_id)
