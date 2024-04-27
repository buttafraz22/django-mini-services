from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from .models import Product, Order, OrderItem

class ProductSerializer(ModelSerializer):
    class Meta:
        model= Product
        fields = ['id', 'name', 'unit_price', 'unit_type']

class OrderItemSerializer(ModelSerializer):
    product_id = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), source='product', write_only=True)
    class Meta:
        model = OrderItem
        fields = ['product_id', 'quantity']


class OrderSerializer(ModelSerializer):
    order_items = OrderItemSerializer(many=True)
    
    class Meta:
        model = Order
        fields = ['customer_name', 'date', 'order_items']