# Generated by Django 5.0.3 on 2024-04-03 19:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerceApp', '0008_order_completed'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='total_quantity',
        ),
    ]