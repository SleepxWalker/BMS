from django.db import models
import traceback

class Client(models.Model):
    business_name = models.CharField(max_length=100)
    contact_name = models.CharField(max_length=100, blank=True)
    email = models.EmailField(unique=True, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    notes = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_general = models.BooleanField(default=False)  # 🔹 מזהה אם זה לקוח כללי
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.is_general:
            print(f"\n🔍 GENERAL CLIENT SAVED: {self.business_name}")
            traceback.print_stack(limit=6)
        super().save(*args, **kwargs)


    def __str__(self):
        return self.business_name or "Unnamed Client"
