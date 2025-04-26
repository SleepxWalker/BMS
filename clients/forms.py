from django import forms
from .models import Client

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['business_name', 'contact_name', 'email', 'phone', 'address', 'notes']
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 3}),
        }