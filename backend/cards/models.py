from django.db import models
from main.settings import CREDIT_CARD_SECRET_KEY
from users.models import User
from cryptography.fernet import Fernet

cipher_suite = Fernet(CREDIT_CARD_SECRET_KEY)

class Card(models.Model):
    class BrandChoices(models.TextChoices):
        VISA = "VISA", "Visa"
        MASTERCARD = "MASTERCARD", "Mastercard"
        AMEX = "AMEX", "American Express"
        ELO = "ELO", "Elo"
        DISCOVER = "DISCOVER", "Discover"

    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="cards")
    card_holder_name = models.CharField(max_length=100)
    
    # Instead of storing full card number, store only last four digits and BIN
    last_four_digits = models.CharField(max_length=4)
    bin = models.CharField(max_length=13, blank=True, null=True)  # First 6 digits (optional)

    expiration_month = models.CharField(max_length=2)
    expiration_year = models.CharField(max_length=4)
    
    brand = models.CharField(max_length=20, choices=BrandChoices.choices)

    # Store encrypted CVV
    _cvv = models.BinaryField(blank=False, null=False)

    active = models.BooleanField(default=True)
    selected = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "cards"
        ordering = ["-created_at"]  # Order by latest cards first

    def __str__(self):
        return f"{self.get_brand_display()} - **** {self.last_four_digits}"

    def set_cvv(self, cvv: str):
        """Encrypt and store CVV securely."""
        encrypted_cvv = cipher_suite.encrypt(cvv.encode())
        self._cvv = encrypted_cvv

    def get_cvv(self) -> str:
        """Decrypt and return CVV (use only when necessary)."""
        return cipher_suite.decrypt(self._cvv).decode()
