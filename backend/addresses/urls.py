from django.urls import path
from .views import create_address, get_addresses, patch_address

urlpatterns = [
    path('addresses/', get_addresses, name='get_addresses'),
    path('addresses/create/', create_address, name='create-address'), 
    path('addresses/update/', patch_address, name='update-address'),
]