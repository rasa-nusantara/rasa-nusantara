from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .forms import ReservationForm
from .models import Reservation
from main.models import Restaurant  # Assuming you have the Restaurant model in the 'main' app
from uuid import UUID
from django.utils import timezone

@login_required
def create_reservation(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)
    
    if request.method == 'POST':
        print("POST request received")  # Debug: memastikan request POST terjadi
        form = ReservationForm(request.POST)
        
        if form.is_valid():
            reservation = form.save(commit=False)
            reservation.user = request.user
            reservation.restaurant = restaurant
            reservation.save()
            return redirect('reservasi:user_reservations')
        else:
            print("Form errors:", form.errors)  # Debug: melihat kesalahan form
    else:
        print("GET request received")  # Debug: memastikan ini adalah request GET
        form = ReservationForm()

    return render(request, 'create_reservation.html', {'form': form, 'restaurant': restaurant})


@login_required
def cancel_reservation(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id, user=request.user)  # Ensure the user owns the reservation

    if request.method == 'POST':
        reservation.delete()  # Delete the reservation
        return redirect('reservasi:user_reservations')  # Redirect to user reservations page after cancellation

    # If the request is GET, return the reservation details for confirmation
    reservation_data = {
        'id': reservation.id,
        'restaurant_name': reservation.restaurant.name,  # Assuming you want to show the restaurant name
        'reservation_date': reservation.reservation_date,
        'reservation_time': reservation.reservation_time,
    }
    return render(request, 'cancel_reservation.html', {'reservation': reservation_data})  # Render confirmation template

@login_required
def user_reservations(request):
    filter_option = request.GET.get('filter', 'all')  # Get the filter option from the request
    reservations = Reservation.objects.filter(user=request.user)

    if filter_option == 'today':
        reservations = reservations.filter(reservation_date=timezone.now().date())
    elif filter_option == 'upcoming':
        reservations = reservations.filter(reservation_date__gt=timezone.now().date())
    elif filter_option == 'due':
        reservations = reservations.filter(reservation_date__lt=timezone.now().date())

    return render(request, 'user_reservations.html', {'reservations': reservations, 'filter_option': filter_option})


@login_required
def edit_reservation(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id, user=request.user)  # Ensure the user owns the reservation

    if request.method == 'POST':
        form = ReservationForm(request.POST, instance=reservation)
        if form.is_valid():
            form.save()  # Save the updated reservation
            return JsonResponse({'success': True, 'message': 'Reservation updated successfully.'})  # Return success response for AJAX
        else:
            return JsonResponse({'success': False, 'errors': form.errors})  # Return errors if form is invalid

    # If the request is GET, return the reservation details for the modal
    reservation_data = {
        'id': reservation.id,
        'reservation_date': reservation.reservation_date,
        'reservation_time': reservation.reservation_time,
        'number_of_people': reservation.number_of_people,
        'special_request': reservation.special_request,
    }
    return JsonResponse({'success': True, 'reservation': reservation_data})  # Return reservation data for AJAX
