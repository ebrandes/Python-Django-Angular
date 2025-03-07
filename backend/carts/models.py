from django.db import models
from products.models import Product
from users.models import User  # Assuming you have a User model

# Your existing Product model


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="cart")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def total_price(self):
        """Calculate total cart price"""
        return sum(item.total_price() for item in self.items.all())

    def clear_cart(self):
        """Clear cart after checkout"""
        self.items.all().delete()

    def __str__(self):
        return f"Cart for {self.user.username}"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def total_price(self):
        """Calculate price for this item"""
        return self.product.price * self.quantity

    def __str__(self):
        return f"{self.quantity} x {self.product.name} in cart"
