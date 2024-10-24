from django import forms
from .models import Review

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']  # Field yang akan ditampilkan di form
        widgets = {
            'rating': forms.NumberInput(attrs={'min': 1, 'max': 5}),  # Input untuk rating antara 1-5
            'comment': forms.Textarea(attrs={'placeholder': 'Tulis review Anda di sini...'}),
        }
