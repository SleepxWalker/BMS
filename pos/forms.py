from django import forms
from .models import Sale, SaleItem

class SaleForm(forms.ModelForm):
    manual_client_name = forms.CharField(
        label="Manual Client Name", required=False
    )

    class Meta:
        model = Sale
        fields = ['client', 'manual_client_name', 'payment_method']


class SaleItemForm(forms.ModelForm):
    class Meta:
        model = SaleItem
        fields = ['item', 'description', 'quantity', 'price_at_time']