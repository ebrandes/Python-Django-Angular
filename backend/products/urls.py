from django.urls import path

from products.views import product_create, product_list, product_update_stock

urlpatterns = [
    path('products/', product_list, name='product-list'),
    path('products/create/', product_create, name='product-create'),
    path('products/stock/update', product_update_stock, name='product-update-stock'),
]