from typing import TYPE_CHECKING
from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from addresses.models import Address
from cards.models import Card
from products.models import Product
from decimal import Decimal
from main.settings import AUTH_USER_MODEL


if TYPE_CHECKING:
    from typing import List
    from .models import CartItem, Cart


class Cart(models.Model):
    """Carrinho de compras vinculado ao usuário"""

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="cart"
    )
    address = models.ForeignKey(
        Address, on_delete=models.SET_NULL, null=True, blank=True
    )
    payment_card = models.ForeignKey(
        Card, on_delete=models.SET_NULL, null=True, blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_total_price(self) -> Decimal:
        """Calcula o total do carrinho"""
        return sum(item.get_total_price() for item in self.items.all())  # type: ignore

    def __str__(self) -> str:
        return f"Carrinho de {self.user.username}"


class CartItem(models.Model):
    """Item do carrinho vinculado ao produto"""

    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def get_total_price(self) -> Decimal:
        """Calcula o preço total desse item"""
        return self.product.price * self.quantity

    def __str__(self) -> str:
        return f"{self.quantity}x {self.product.name} no carrinho de {self.cart.user.username}"
