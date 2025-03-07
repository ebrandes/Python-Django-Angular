from rest_framework import serializers
from models import Cart, CartItem


class CartItemSerializer(serializers.ModelSerializer):
    product_name = serializers.ReadOnlyField(source="product.name")
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = ["id", "product", "product_name", "quantity", "total_price"]

    def get_total_price(self, obj):
        return obj.total_price()


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ["id", "user", "items", "total_price", "created_at"]

    def get_total_price(self, obj):
        return obj.total_price()
