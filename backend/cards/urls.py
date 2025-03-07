from django.urls import path
from .views import card_list, create_card

urlpatterns = [
    path('cards/create/', create_card, name="cards_create"),  
    path('cards/', card_list, name="card_list"),
]
