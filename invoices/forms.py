from django import forms
from .models import Invoice, InvoiceItem

class InvoiceItemForm(forms.ModelForm):
    price = forms.DecimalField(label='Price', max_digits=10, decimal_places=2)

    class Meta:
        model = InvoiceItem
        fields = ['item', 'description', 'quantity', 'price']

    def clean(self):
        cleaned_data = super().clean()
        if 'price' in cleaned_data:
            cleaned_data['price_at_time'] = cleaned_data['price']
        return cleaned_data

class InvoiceForm(forms.ModelForm):
    client_name = forms.CharField(required=False, label="Client Name (manual)")

    class Meta:
        model = Invoice
        fields = ['client', 'client_name', 'due_date', 'status']