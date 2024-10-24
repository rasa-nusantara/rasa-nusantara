from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import ReviewForm
from .models import Review
from django.http import HttpResponseNotFound , HttpResponseRedirect
from django.urls import reverse



@login_required
def add_review(request, restaurant_name):
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)  # Menyimpan form tapi tidak langsung ke database
            review.user = request.user  # Mengaitkan review dengan pengguna yang login
            review.restaurant_name = restaurant_name  # Menggunakan nama restoran dari dummy data
            review.save()  # Simpan review ke database
            return redirect('restaurant_review', name=restaurant_name)  # Redirect setelah submit
    else:
        form = ReviewForm()

    context = {
        'restaurant_name': restaurant_name,
        'form': form
    }

    return render(request, 'add_review.html', context)

def edit_review(request, id):
    # Get review berdasarkan id
    review = Review.objects.get(pk=id)

    # Set review sebagai instance dari form
    form = ReviewForm(request.POST or None, instance=review)

    if form.is_valid() and request.method == "POST":
        # Simpan perubahan form dan redirect ke halaman review restoran
        form.save()
        # Pastikan review.restaurant_name diteruskan dengan benar
        return HttpResponseRedirect(reverse('restaurant_review', kwargs={'name': review.restaurant_name}))

    # Pastikan 'restaurant_name' diteruskan ke template jika dibutuhkan
    context = {
        'form': form,
        'restaurant_name': review.restaurant_name  # Kirim nama restoran ke template
    }
    return render(request, "edit_review.html", context)

def delete_review(request, id):
    # Get review berdasarkan id
    review = Review.objects.get(pk=id)

    # Hapus review
    review.delete()

    # Redirect ke halaman review restoran setelah review dihapus
    return HttpResponseRedirect(reverse('restaurant_review', kwargs={'name': review.restaurant_name}))

def restaurant_list(request):
    # Dummy data untuk daftar restoran
    restaurants = [
        {
            'id': 1,
            'name': 'Restoran Dummy 1',
            'location': 'Jalan Dummy Nomor 1',
            'average_price': 50000,
            'rating': 4.5
        },
        {
            'id': 2,
            'name': 'Restoran Dummy 2',
            'location': 'Jalan Dummy Nomor 2',
            'average_price': 60000,
            'rating': 4.0
        }
    ]

    # Mengirimkan data sebagai context ke template
    context = {
        'restaurants': restaurants
    }
    
    return render(request, 'restaurant_list.html', context)


def restaurant_review(request, name):
    # Dummy data untuk restoran
    restaurant = next((r for r in [
        {
            'id': 1,
            'name': 'Restoran Dummy 1',
            'location': 'Jalan Dummy Nomor 1',
            'average_price': 50000,
            'rating': 4.5,
            'reviews': [
                {'reviewer': 'User A', 'comment': 'Makanannya enak, pelayanannya baik.'},
                {'reviewer': 'User B', 'comment': 'Tempatnya nyaman.'}
            ]
        },
        {
            'id': 2,
            'name': 'Restoran Dummy 2',
            'location': 'Jalan Dummy Nomor 2',
            'average_price': 60000,
            'rating': 4.0,
            'reviews': [
                {'reviewer': 'User C', 'comment': 'Pelayanannya lambat, tapi makanannya enak.'}
            ]
        }
    ] if r['name'] == name), None)

    if not restaurant:
        return HttpResponseNotFound("Restoran tidak ditemukan.")

    # Ambil review dari database yang sesuai dengan nama restoran
    user_reviews = Review.objects.filter(restaurant_name=name)

    # Gabungkan review dari dummy data dan review dari database
    all_reviews = restaurant['reviews'] + [
        {'reviewer': review.user.username, 'comment': review.comment, 'id': review.id} for review in user_reviews
    ]

    context = {
        'restaurant': restaurant,
        'reviews': all_reviews  # Semua review (dummy + dari database)
    }
    return render(request, 'restaurant_review.html', context)



