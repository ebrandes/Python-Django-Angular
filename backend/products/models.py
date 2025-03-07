from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)  
    stock = models.PositiveIntegerField(default=0)  
    is_available = models.BooleanField(default=True)  
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - ${self.price} (Stock: {self.stock})"

    def update_stock(self, quantity_sold):
        """Reduce stock when a sale is made."""
        if self.stock >= quantity_sold:
            self.stock -= quantity_sold
            if self.stock == 0:
                self.is_available = False
            self.save()
        else:
            raise ValueError("Not enough stock available")
