from django.db import models

# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=200)
    unit_price = models.FloatField(default=0.0)
    unit_type = models.BooleanField(default=True)
    stock=models.PositiveIntegerField(default=1)

class Order(models.Model):
    customer_name = models.CharField(max_length=200)
    date = models.DateTimeField(auto_now_add=True)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

