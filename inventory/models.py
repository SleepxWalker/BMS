from django.db import models

class InventoryTransaction(models.Model):
    TRANSACTION_TYPES = [
        ('sale', 'Sale'),
        ('restock', 'Restock'),
        ('adjustment', 'Adjustment'),
    ]

    item = models.ForeignKey('Inventory', on_delete=models.CASCADE, related_name='transactions')
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPES)
    quantity_changed = models.IntegerField()
    related_sale = models.ForeignKey(
        'pos.Sale',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='inventory_transactions_inventory'
    )
    note = models.CharField(max_length=255, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.transaction_type} - {self.quantity_changed} units on {self.timestamp.strftime('%Y-%m-%d %H:%M')}"

class Inventory(models.Model):
    product_name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    category = models.CharField(max_length=50)
    quantity = models.PositiveIntegerField(default=0)
    reorder_level = models.PositiveIntegerField(default=10)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_general = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.product_name