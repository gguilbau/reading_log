from django import forms
from .models import BookRead

class BookReadForm(forms.ModelForm):
    class Meta:
        model = BookRead
        fields = ["title", "author", "length"]