from django.db.models.signals import post_migrate
from django.dispatch import receiver
from .models import Client

@receiver(post_migrate)
def ensure_general_client_exists(sender, **kwargs):
    if not Client.objects.filter(is_general=True).exists():
        Client.objects.create(
            business_name="General Client",
            is_general=True
        )
        print("✅ Created default General Client.")