from django import forms
from .models import Restaurant, Menu

class RestaurantForm(forms.ModelForm):
    class Meta:
        model = Restaurant
        fields = ['name', 'address', 'rating', 'harga_rata_rata']

class MenuForm(forms.ModelForm):
    class Meta:
        model = Menu
        fields = ['restaurant', 'name', 'price']
