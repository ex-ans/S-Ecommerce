# Generated by Django 5.0.3 on 2024-04-06 20:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerceApp', '0014_cart_submitted'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cart',
            name='submitted',
        ),
    ]