# Generated by Django 5.1.7 on 2025-03-22 10:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inventory',
            name='description',
            field=models.TextField(blank=True, default='non'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='inventory',
            name='quantity',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='inventory',
            name='reorder_level',
            field=models.PositiveIntegerField(default=10),
        ),
    ]
