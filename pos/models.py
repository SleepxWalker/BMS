from django.db import models
from inventory.models import Inventory
from clients.models import Client

class Sale(models.Model):
    client = models.ForeignKey(Client, on_delete=models.SET_NULL, null=True, blank=True)
    manual_client_name = models.CharField(max_length=100, blank=True, null=True)
    sale_date = models.DateTimeField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    payment_method = models.CharField(
        max_length=20,
        choices=[
            ('cash', 'Cash'),
            ('card', 'Card'),
            ('transfer', 'Bank Transfer'),
            ('other', 'Other'),
        ],
        default='cash'
    )

    def __str__(self):
        return f"Sale #{self.pk} - {self.manual_client_name or (self.client and self.client.business_name) or 'Unknown'}"


class SaleItem(models.Model):
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE, related_name='items')
    item = models.ForeignKey(Inventory, on_delete=models.SET_NULL, null=True, blank=True)
    description = models.CharField(max_length=255, blank=True)
    quantity = models.PositiveIntegerField()
    price_at_time = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def get_total(self):
        return self.quantity * self.price_at_time

    def __str__(self):
        return f"{self.quantity} x {self.item or self.description}"


class InventoryTransaction(models.Model):
    TRANSACTION_TYPES = [
        ('sale', 'Sale'),
        ('manual', 'Manual Adjustment'),
        ('purchase', 'Purchase'),
    ]

    item = models.ForeignKey(Inventory, on_delete=models.CASCADE)
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPES)
    quantity_changed = models.IntegerField()  # חיובי או שלילי
    related_sale = models.ForeignKey(
        'pos.Sale',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='inventory_transactions_pos'
    )
    note = models.CharField(max_length=255, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.transaction_type.title()} - {self.item.product_name} ({self.quantity_changed})"