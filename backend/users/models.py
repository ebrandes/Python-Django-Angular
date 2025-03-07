from django.contrib.auth.models import AbstractUser
from django.db import models

from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    """Custom User Model with additional fields"""
    username = None  # Remove username, we will use email instead
    email = models.EmailField(unique=True, blank=False)
    role = models.CharField(max_length=50, default="user")

    USERNAME_FIELD = "email"  # Set email as the login field
    REQUIRED_FIELDS = ["first_name", "last_name"]  # Required when creating users

    class Meta:
        """Define table name and default ordering"""
        db_table = "users"  # Custom table name in MySQL
        ordering = ["first_name", "last_name"]  # Default ordering

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
