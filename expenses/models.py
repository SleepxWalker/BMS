from django.db import models

class Expense(models.Model):
    CATEGORY_CHOICES = [
        ('office', 'Office Supplies'),
        ('marketing', 'Marketing'),
        ('salary', 'Salaries'),
        ('rent', 'Rent'),
        ('utilities', 'Utilities'),
        ('other', 'Other'),
    ]

    description = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='other')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.description} - ${self.amount}"