from django import forms
from .models import MenuItem

class MenuItemForm(forms.ModelForm):
    categories = forms.CharField(
        required=False,
        label="Categories (comma-separated)",
        widget=forms.TextInput(attrs={'placeholder': 'e.g. Mie, Nasi'})
    )

    class Meta:
        model = MenuItem
        fields = ['name']  # Only include 'name' directly from the MenuItem model

    def clean_categories(self):
        # Simply return the cleaned category input as is
        return self.cleaned_data['categories']
