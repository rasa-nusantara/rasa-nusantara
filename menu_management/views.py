from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from .models import MenuItem, Restaurant, Category  # Pastikan Category diimpor
from .forms import MenuItemForm

@staff_member_required(login_url='main:login')
def admin_menu_view(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)
    menu_items = restaurant.menu_items.all()  # Mengambil semua menu item yang terkait dengan restoran ini
    context = {
        'restaurant': restaurant,
        'menu_items': menu_items,
    }
    return render(request, 'menu_management/admin_menu.html', context)



@staff_member_required(login_url='main:login')
def add_menu(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)
    if request.method == 'POST':
        form = MenuItemForm(request.POST)
        if form.is_valid():
            menu_item = form.save(commit=False)
            menu_item.restaurant = restaurant
            menu_item.save()  # Simpan MenuItem tanpa kategori dulu
            form.save_m2m()  # Simpan relasi many-to-many (kategori)
            messages.success(request, 'Menu item added successfully!')
            return redirect('menu_management:admin_menu', restaurant_id=restaurant_id)
    else:
        form = MenuItemForm()

    context = {
        'form': form,
        'restaurant': restaurant,
        'categories': Category.objects.all(),  # Mengambil semua kategori untuk form
    }
    return render(request, 'menu_management/add_menu.html', context)


@staff_member_required(login_url='main:login')
def edit_menu(request, restaurant_id, id):
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)
    menu_item = get_object_or_404(MenuItem, id=id, restaurant=restaurant)
    if request.method == 'POST':
        form = MenuItemForm(request.POST, instance=menu_item)
        if form.is_valid():
            form.save()
            form.save_m2m()  # Simpan perubahan pada relasi many-to-many (kategori)
            messages.success(request, 'Menu item updated successfully!')
            return redirect('menu_management:admin_menu', restaurant_id=restaurant_id)
    else:
        form = MenuItemForm(instance=menu_item)

    context = {
        'form': form,
        'restaurant': restaurant,
        'menu_item': menu_item,
        'categories': Category.objects.all(),  # Kategori juga diperlukan di sini
    }
    return render(request, 'menu_management/edit_menu.html', context)


@staff_member_required(login_url='main:login')
def delete_menu(request, restaurant_id, id):
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)
    menu_item = get_object_or_404(MenuItem, id=id, restaurant=restaurant)
    menu_item.delete()
    messages.success(request, 'Menu item deleted successfully!')
    return redirect('menu_management:admin_menu', restaurant_id=restaurant_id)
