from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse
from django.core import serializers
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.http import HttpResponseRedirect
import datetime

from main.models import Restaurant

def homepage(request):
    restaurants = Restaurant.objects.all()
    context = {
        'restaurants': restaurants
    }
    return render(request, 'main.html', context)
# def register(request):
#     form = UserCreationForm()

#     if request.method == "POST":
#         form = UserCreationForm(request.POST)
#         if form.is_valid():
#             form.save()
#             messages.success(request, 'Your account has been successfully created!')
#             return redirect('main:login')
#     context = {'form':form}
#     return render(request, 'register.html', context)

# def login_user(request):
#    if request.method == 'POST':
#       form = AuthenticationForm(data=request.POST)
#       if form.is_valid():
#         user = form.get_user()
#         login(request, user)
#         response = HttpResponseRedirect(reverse("main:homepage"))
#         response.set_cookie('last_login', str(datetime.datetime.now()))
#         return response

#    else:
#       form = AuthenticationForm(request)
#    context = {'form': form}
#    return render(request, 'login.html', context)

# def logout_user(request):
#     logout(request)
#     response = HttpResponseRedirect(reverse('main:login'))
#     response.delete_cookie('last_login')
#     return response