from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from main.models import Restaurant, MenuItem, Category
from .forms import MenuItemForm

def handle_categories(menu_item, category_names):
    """Function to handle category assignment."""
    menu_item.categories.clear()  # Clear existing categories
    for name in category_names:
        name = name.strip()  # Remove any extra whitespace
        if name:  # Only add non-empty names
            category, created = Category.objects.get_or_create(name=name)
            menu_item.categories.add(category)  # Associate with the menu item

@user_passes_test(lambda u: u.is_staff, login_url='main:login')
def admin_menu_view(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)  # Ensure it uses UUID
    menu_items = restaurant.menu_items.all()  # Get the menu items for the restaurant
    context = {
        'restaurant': restaurant,
        'menu_items': menu_items,
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

            # Handle categories
            category_names = request.POST.get('categories', '').split(',')
            handle_categories(menu_item, category_names)  # Reuse the function

            messages.success(request, 'Menu item added successfully!')
            return redirect('adminview:admin_menu', restaurant.id)
    else:
        form = MenuItemForm()
    return render(request, 'menu_management/add_menu.html', {'form': form, 'restaurant': restaurant})

@user_passes_test(lambda u: u.is_staff, login_url='main:login')
def edit_menu(request, restaurant_id, id):
    menu_item = get_object_or_404(MenuItem, id=id, restaurant__id=restaurant_id)
    
    if request.method == 'POST':
        form = MenuItemForm(request.POST, instance=menu_item)
        if form.is_valid():
            updated_item = form.save(commit=False)
            updated_item.restaurant = menu_item.restaurant  # Maintain the restaurant association
            updated_item.save()

            # Handle categories
            category_names = request.POST.get('categories', '').split(',')
            handle_categories(updated_item, category_names)  # Reuse the function

            messages.success(request, 'Menu item updated successfully!')
            return redirect('adminview:admin_menu', restaurant_id=restaurant_id)
    else:
        form = MenuItemForm(instance=menu_item)

    return render(request, 'menu_management/edit_menu.html', {
        'form': form,
        'restaurant': menu_item.restaurant,
        'menu_item': menu_item,
    })

@user_passes_test(lambda u: u.is_staff, login_url='main:login')
def delete_menu(request, restaurant_id, id):
    menu_item = get_object_or_404(MenuItem, id=id, restaurant__id=restaurant_id)
    menu_item.delete()
    messages.success(request, 'Menu item deleted successfully!')
    return redirect('adminview:admin_menu', restaurant_id=restaurant_id)
