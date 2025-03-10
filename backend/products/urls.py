from django.urls import path
from .views import ProductListView, ProductUpdateStockView

urlpatterns = [
    path("products/", ProductListView.as_view(), name="product-list"),
    path(
        "products/update-stock/",
        ProductUpdateStockView.as_view(),
        name="product-update-stock",
    ),
]
