from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import ReviewForm
from .models import Review
from django.http import HttpResponseNotFound, HttpResponseRedirect
from django.urls import reverse
from main.models import Restaurant
from django.http import JsonResponse

@login_required
# def add_review(request, restaurant_name):
#     # Mendapatkan restoran berdasarkan nama
#     restaurant = get_object_or_404(Restaurant, name=restaurant_name)

#     if request.method == 'POST':
#         form = ReviewForm(request.POST)
#         if form.is_valid():
#             review = form.save(commit=False)  # Menyimpan form tanpa langsung ke database
#             review.user = request.user  # Mengaitkan review dengan pengguna yang login
#             review.restaurant_name = restaurant.name  # Menggunakan nama restoran dari objek
#             review.save()  # Simpan review ke database
#             return redirect('restaurant_review', name=restaurant.name)  # Redirect setelah submit
#     else:
#         form = ReviewForm()

#     context = {
#         'restaurant_name': restaurant.name,
#         'form': form
#     }

#     return render(request, 'add_review.html', context)
def add_review_ajax(request, restaurant_name):
    restaurant = get_object_or_404(Restaurant, name=restaurant_name)

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.restaurant_name = restaurant.name
            review.save()
            
            # Respond with the new review data
            response_data = {
                'reviewer': review.user.username,
                'comment': review.comment,
                'rating': review.rating
            }
            return JsonResponse(response_data)

    return JsonResponse({'error': 'Invalid form'}, status=400)


def edit_review(request, id):
    # Mendapatkan review berdasarkan id
    review = get_object_or_404(Review, pk=id)

    # Set review sebagai instance dari form
    form = ReviewForm(request.POST or None, instance=review)

    if form.is_valid() and request.method == "POST":
        form.save()
        # Redirect ke halaman review restoran setelah perubahan disimpan
        return HttpResponseRedirect(reverse('restaurant_review', kwargs={'name': review.restaurant_name}))

    context = {
        'form': form,
        'restaurant_name': review.restaurant_name  # Mengirimkan nama restoran ke template
    }
    return render(request, "edit_review.html", context)


def delete_review(request, id):
    # Mendapatkan review berdasarkan id
    review = get_object_or_404(Review, pk=id)

    # Hapus review
    review.delete()

    # Redirect ke halaman review restoran setelah review dihapus
    return HttpResponseRedirect(reverse('restaurant_review', kwargs={'name': review.restaurant_name}))



def restaurant_review(request, name):
    # Mendapatkan restoran berdasarkan nama
    restaurant = get_object_or_404(Restaurant, name=name)

    # Mendapatkan semua review untuk restoran ini dari database
    user_reviews = Review.objects.filter(restaurant_name=name)
    menu_items = restaurant.menu_items.all()

    form = ReviewForm
    context = {
        'restaurant': restaurant,
        'reviews': user_reviews, # Semua review dari database
        'menu_items' : menu_items,
        'form': form
    }
    return render(request, 'restaurant_review.html', context)

def edit_review_ajax(request):
    if request.method == 'POST':
        review_id = request.POST.get('review_id')
        review = get_object_or_404(Review, id=review_id, user=request.user)
        review.rating = request.POST.get('rating')
        review.comment = request.POST.get('comment')
        review.save()
        return JsonResponse({
            'id': review.id,
            'rating': review.rating,
            'comment': review.comment,
            'username': review.user.username, 
        })
    return JsonResponse({'error': 'Invalid request'}, status=400)


