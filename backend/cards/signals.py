from django.dispatch import receiver
from django.db.models.signals import post_save
from cards.models import Card
from cart.models import Cart


@receiver(post_save, sender=Card)
def remove_address_from_cart(sender, instance, **kwargs):
    if not instance.active:
        Cart.objects.filter(card=instance).update(card=None)
