from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from .models import MenuItem, Restaurant
from .forms import MenuItemForm

# Admin view for all menu items for a restaurant
@staff_member_required(login_url='main:login')
def admin_menu_view(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)
    menu_items = restaurant.menu_items.all()
    return render(request, 'menu_management/admin_menu.html', {'menu_items': menu_items, 'restaurant': restaurant})

# Add menu item view
@staff_member_required(login_url='main:login')
def add_menu(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)
    if request.method == 'POST':
        form = MenuItemForm(request.POST)
        if form.is_valid():
            menu_item = form.save(commit=False)
            menu_item.restaurant = restaurant
            menu_item.save()
            messages.success(request, 'Menu item added successfully!')
            return redirect('menu_management:admin_menu', restaurant_id=restaurant_id)
    else:
        form = MenuItemForm()
    return render(request, 'menu_management/add_menu.html', {'form': form, 'restaurant': restaurant})

# Edit menu item view
@staff_member_required(login_url='main:login')
def edit_menu(request, restaurant_id, id):
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)
    menu_item = get_object_or_404(MenuItem, id=id, restaurant=restaurant)
    if request.method == 'POST':
        form = MenuItemForm(request.POST, instance=menu_item)
        if form.is_valid():
            form.save()
            messages.success(request, 'Menu item updated successfully!')
            return redirect('menu_management:admin_menu', restaurant_id=restaurant_id)
    else:
        form = MenuItemForm(instance=menu_item)
    return render(request, 'menu_management/edit_menu.html', {'form': form, 'menu_item': menu_item, 'restaurant': restaurant})

# Delete menu item view
@staff_member_required(login_url='main:login')
def delete_menu(request, restaurant_id, id):
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)
    menu_item = get_object_or_404(MenuItem, id=id, restaurant=restaurant)
    menu_item.delete()
    messages.success(request, 'Menu item deleted successfully!')
    return redirect('menu_management:admin_menu', restaurant_id=restaurant_id)
