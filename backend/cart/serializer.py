from rest_framework import serializers
from addresses.models import Address
from cards.models import Card
from .models import Cart, CartItem


class CartItemSerializer(serializers.ModelSerializer):
    """Serializa os itens do carrinho"""

    product_name = serializers.CharField(source="product.name", read_only=True)
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = ["id", "product", "product_name", "quantity", "total_price"]

    def get_total_price(self, obj):
        return obj.get_total_price()


class CartSerializer(serializers.ModelSerializer):
    """Serializa o carrinho completo"""

    items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField()
    address = serializers.PrimaryKeyRelatedField(
        queryset=Address.objects.all(), allow_null=True
    )
    payment_card = serializers.PrimaryKeyRelatedField(
        queryset=Card.objects.all(), allow_null=True
    )

    class Meta:
        model = Cart
        fields = ["id", "user", "items", "total_price", "address", "payment_card"]

    def get_total_price(self, obj):
        return obj.get_total_price()
