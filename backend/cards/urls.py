from django.urls import path
from .views import card_list, card_create, card_update

urlpatterns = [
    path('cards/create/', card_create, name="cards_create"),  
    path('cards/update/', card_update, name="cards_update"),
    path('cards/', card_list, name="card_list"),
]
