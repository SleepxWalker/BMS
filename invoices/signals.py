from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import InvoiceItem
from inventory.models import Inventory

@receiver([post_save, post_delete], sender=InvoiceItem)
def update_invoice_total(sender, instance, **kwargs):
    invoice = instance.invoice
    total = sum(item.get_total() for item in invoice.items.all())
    invoice.total_amount = total
    invoice.save()

@receiver(post_save, sender=InvoiceItem)
def decrease_inventory_on_create(sender, instance, created, **kwargs):
    if created and instance.item and not instance.item.is_general:
        inventory_item = instance.item
        inventory_item.quantity -= instance.quantity
        inventory_item.save()