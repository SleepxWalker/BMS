# Generated by Django 5.1.7 on 2025-04-19 18:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pos', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='sale',
            old_name='sale_time',
            new_name='sale_date',
        ),
        migrations.RenameField(
            model_name='saleitem',
            old_name='price_at_time',
            new_name='price_at_sale',
        ),
        migrations.RemoveField(
            model_name='sale',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='saleitem',
            name='description',
        ),
        migrations.AddField(
            model_name='sale',
            name='payment_method',
            field=models.CharField(choices=[('cash', 'Cash'), ('credit', 'Credit Card'), ('transfer', 'Bank Transfer')], default='cash', max_length=30),
        ),
        migrations.AddField(
            model_name='saleitem',
            name='manual_item_name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
