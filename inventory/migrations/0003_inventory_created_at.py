# Generated by Django 5.1.7 on 2025-03-22 17:37

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0002_alter_inventory_description_alter_inventory_quantity_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='inventory',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2025, 3, 22, 17, 35, 10, 949365, tzinfo=datetime.timezone.utc)),
            preserve_default=False,
        ),
    ]
