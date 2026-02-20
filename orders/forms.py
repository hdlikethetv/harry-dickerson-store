from django import forms
from .models import Order


class OrderCreateForm(forms.ModelForm):
    """
    Form for collecting shipping information during checkout.
    """
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'email', 'address', 'postal_code', 'city', 'country']
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Last Name'}),
            'email': forms.EmailInput(attrs={'placeholder': 'email@example.com'}),
            'address': forms.TextInput(attrs={'placeholder': 'Street Address'}),
            'postal_code': forms.TextInput(attrs={'placeholder': 'Postal Code'}),
            'city': forms.TextInput(attrs={'placeholder': 'City'}),
            'country': forms.TextInput(attrs={'placeholder': 'Country'}),
        }