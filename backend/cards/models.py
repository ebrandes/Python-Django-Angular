from turtle import mode
from django.db import models

from users.models import User


# Create your models here.
class Card(models.Model):

    class Meta:
        db_table = "cards"
        ordering = ["-created_at"]

    class Branch(models.TextChoices):
        VISA = "VISA"
        MASTERCARD = "MASTERCARD"

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    last_four_digits = models.CharField(max_length=4)
    holder = models.CharField(max_length=100)
    expiry_year = models.CharField(max_length=4)
    expiry_month = models.CharField(max_length=3)
    branch = models.CharField(max_length=20, choices=Branch.choices)
    is_default = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.branch.value + "****" + self.last_four_digits

    def save(self, *args, **kwargs):
        if self.is_default:
            Card.objects.filter(user=self.user).update(is_default=False)
        super().save(*args, **kwargs)
