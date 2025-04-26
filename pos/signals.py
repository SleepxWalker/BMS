from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import SaleItem
from inventory.models import InventoryTransaction


@receiver(post_save, sender=SaleItem)
def handle_sale_item_creation(sender, instance, created, **kwargs):
    """
    Handles inventory deduction and logs transaction when a new SaleItem is created.
    """
    if created and instance.item and not instance.item.is_general:
        item = instance.item

        # אבטחה נגד ירידה לכמות שלילית
        if item.quantity < instance.quantity:
            raise ValueError(f"Insufficient stock for item {item.product_name}.")

        # עדכון כמות במלאי
        item.quantity -= instance.quantity
        item.save()

        # תיעוד תנועה
        InventoryTransaction.objects.create(
            item=item,
            transaction_type='sale',
            quantity_changed=-instance.quantity,
            related_sale=instance.sale,
            note='Sale deduction'
        )