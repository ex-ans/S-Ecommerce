# Generated by Django 5.0.3 on 2024-03-30 15:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerceApp', '0004_alter_products_stock'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='price',
            field=models.IntegerField(default=0),
        ),
    ]