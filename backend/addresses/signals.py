from django.dispatch import receiver
from django.db.models.signals import post_save
from addresses.models import Address
from cart.models import Cart


@receiver(post_save, sender=Address)
def remove_address_from_cart(sender, instance, **kwargs):
    if not instance.active:
        Cart.objects.filter(address=instance).update(address=None)
