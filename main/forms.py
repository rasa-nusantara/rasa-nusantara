from django import forms
from .models import Restaurant, Menu
from django.forms import inlineformset_factory

class RestaurantForm(forms.ModelForm):
    class Meta:
        model = Restaurant
        fields = ['name', 'address', 'rating', 'harga_rata_rata']  

MenuFormSet = inlineformset_factory(
    Restaurant, 
    Menu,       
    fields=['name'],  
    extra=1,  
    can_delete=True  
)