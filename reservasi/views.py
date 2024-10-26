from django.shortcuts import render

# Create your views here.

from django.shortcuts import render, redirect
from .forms import ReservationForm


def index(request):
    return render(request, 'index.html')

def create_reservation(request):
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            reservation = form.save(commit=False)
            reservation.user = request.user  # Assign the logged-in user to the reservation
            reservation.save()
            return redirect('reservation_success')  # Redirect to a success page after the reservation
    else:
        form = ReservationForm()

    return render(request, 'create_reservation.html', {'form': form})
