from django.db import models
import datetime

# Create your models here.
class Products(models.Model):
    product_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField(default='No description available')
    image = models.ImageField(upload_to='product_image')
    price = models.IntegerField()
    stock = models.IntegerField(default=0)
    def __str__ (self):
        return self.name
    
class Cart(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    price = models.IntegerField(default=0)
    def __str__(self):
        return f"{self.product.name} - Quantity: {self.quantity}"
    

class Order(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, default=None)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length = 100)
    email = models.EmailField(default=None)
    address = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=100)
    completed = models.BooleanField(default=False)
    def __str__(self):
        return f"Order {self.id} - {self.cart.user.username} - Total Price: ${self.total_price} - {self.cart.product.name}"
