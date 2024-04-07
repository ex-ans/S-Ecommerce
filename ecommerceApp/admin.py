from django.contrib import admin
from ecommerceApp.models import Products, Cart, Order

# Register your models here.
admin.site.register(Products)
admin.site.register(Order)
@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['display_name']

    def display_name(self, obj):
        return f"{obj.id} - {obj.product.name} - Quantity: {obj.quantity}"
    