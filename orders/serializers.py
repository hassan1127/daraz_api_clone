from rest_framework import serializers
from .models import Order, OrderItem
from products.serializers import ProductSerializer


class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    subtotal = serializers.DecimalField(
        max_digits=10, decimal_places=2, read_only=True   # ← property
    )

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'quantity', 'subtotal']


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    item_count = serializers.IntegerField(read_only=True)   # ← property
    is_pending = serializers.BooleanField(read_only=True)   # ← property

    class Meta:
        model = Order
        fields = ['id', 'status', 'total', 'item_count', 'is_pending', 'items', 'created_at']

 
        