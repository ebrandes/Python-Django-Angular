from django.urls import path
from cards.views import CardsView

urlpatterns = [
    path("cards/", CardsView.as_view(), name="cards"),
]
