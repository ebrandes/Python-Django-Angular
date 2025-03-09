from typing import TYPE_CHECKING
from django.db import models
from products.models import Product
from users.models import User  # Assuming you have a User model
from decimal import Decimal

if TYPE_CHECKING:
    from .models import CartItem  # Ensure Pylance recognizes the correct type


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="cart")
    created_at = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(
        max_digits=10, decimal_places=2, default=Decimal("0.00")
    )

    def get_total_price(self) -> Decimal:
        """Calculate total cart price"""
        items: list["CartItem"] = list(self.items.all())  # type: ignore # Force explicit typing
        return sum(item.total_price() for item in items)  # type: ignore # Call method correctly

    def clear_cart(self):
        """Clear cart after checkout"""
        self.items.all().delete()  # type: ignore

    def __str__(self):
        return f"Cart for {self.user.username}"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def total_price(self) -> Decimal:
        """Calculate price for this item"""
        return self.product.price * self.quantity

    def __str__(self):
        return f"{self.quantity} x {self.product.name} in cart"
