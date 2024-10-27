from django import forms
from main.models import MenuItem

class MenuItemForm(forms.ModelForm):
    class Meta:
        model = MenuItem
        fields = ['name']  
        widgets = {
            'name': forms.TextInput(attrs={'class': 'border rounded-lg w-full py-2 px-3 text-gray-700'}),
        }
