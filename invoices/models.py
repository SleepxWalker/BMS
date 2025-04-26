from django.db import models
from clients.models import Client
from inventory.models import Inventory
from projects.models import Project
from tasks.models import Task

class Invoice(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, null=True, blank=True)
    manual_client_name = models.CharField(max_length=100, blank=True, null=True)
    issue_date = models.DateField(auto_now_add=True)
    due_date = models.DateField()
    project = models.ForeignKey(Project, on_delete=models.SET_NULL, null=True, blank=True)
    task = models.ForeignKey(Task, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(
        max_length=20,
        choices=[('Draft', 'Draft'), ('Sent', 'Sent'), ('Paid', 'Paid')],
        default='Draft'
    )

    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.client:
            return f"Invoice #{self.pk} - {self.client.business_name}"
        elif self.manual_client_name:
            return f"Invoice #{self.pk} - {self.manual_client_name}"
        return f"Invoice #{self.pk}"


class InvoiceItem(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='items')
    item = models.ForeignKey(Inventory, on_delete=models.SET_NULL, null=True, blank=True)
    manual_item_name = models.CharField(max_length=100, blank=True, null=True)
    description = models.CharField(max_length=255, blank=True)
    quantity = models.PositiveIntegerField()
    price_at_time = models.DecimalField(max_digits=10, decimal_places=2)

    def get_total(self):
        return self.quantity * self.price_at_time

    def __str__(self):
        return f"{self.quantity} x {self.item or self.manual_item_name or self.description} @ {self.price_at_time}"