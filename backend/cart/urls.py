from django.urls import path
from .views import CartView, AddToCartView, CheckoutView

urlpatterns = [
    path("cart/", CartView.as_view(), name="cart"),
    path("cart/add/", AddToCartView.as_view(), name="add-to-cart"),
    path("cart/checkout/", CheckoutView.as_view(), name="checkout"),
]
