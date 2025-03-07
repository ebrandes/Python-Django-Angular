from django.urls import path

from views import add_to_cart, checkout, get_cart, remove_from_cart

urlpatterns = [
    path("cart/add", add_to_cart, name="add_to_cart"),
    path("cart/remove", remove_from_cart, name="remove_from_cart"),
    path("cart/", get_cart, name="get_cart"),
    path("cart/checkout", checkout, name="checkout"),
]
