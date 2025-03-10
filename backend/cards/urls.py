from django.urls import path
from cards.views import CardsView

urlpatterns = [
    path("cards/", CardsView.as_view(), name="cards"),
    # path("cards/<int:pk>/", CardsView.as_view(), name="card"),
]
