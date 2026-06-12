from rest_framework import serializers
from .models import Product, Category


class CategorySerializer(serializers.ModelSerializer):
    seller = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'parent', 'seller']
        read_only_fields = ['seller']


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), source='category', write_only=True
    )
    seller = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'description', 'price',
            'stock', 'category', 'category_id',
            'seller', 'created_at'
        ]
        read_only_fields = ['seller']