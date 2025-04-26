from django import forms
from .models import Inventory

class InventoryForm(forms.ModelForm):
    class Meta:
        model = Inventory
        fields = ['product_name', 'description', 'category', 'quantity', 'reorder_level', 'price']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }