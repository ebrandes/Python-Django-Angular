from functools import partial
from cards.models import Card
from cards.serialize import CardSerializer
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from helpers.swagger import get_auth_header

@swagger_auto_schema(
    method='post',
    operation_summary="Create a New Card",
    operation_description="Create a new card with the provided data.",
    manual_parameters=[get_auth_header()],
    request_body=CardSerializer,
    responses={201: CardSerializer(), 400: "Invalid input"}
)
@api_view(['POST'])
def card_create(request) :
    """Handles POST (create card)"""
    if request.method == 'POST':
        serializer = CardSerializer(data=request.data)
        if serializer.is_valid():
            card = serializer.save()
            return Response(CardSerializer(card).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@swagger_auto_schema(
    method='PATCH',
    operation_summary="Update Card",
    operation_description="Update a card with the provided data.",
    manual_parameters=[get_auth_header()],
    request_body=CardSerializer,
    responses={200: CardSerializer(), 400: "Invalid input"}
)
@api_view(['PATCH'])
def card_update(request):
    """Handles PATCH (update card)"""
    card_id = request.data.get("id")  # Extract ID from the request body

    if not card_id:
        return Response({"error": "Card ID is required in the request body"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        cards = Card.objects.filter(user=request.user)
        for card in cards:
            card.selected = False
            card.save()
            
        card = cards.get(id=card_id)  # Retrieve the card instance
    except Card.DoesNotExist:
        return Response({"error": "Card not found"}, status=status.HTTP_404_NOT_FOUND)

    serializer = CardSerializer(card, data=request.data, partial=True)  # Allow partial updates

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@swagger_auto_schema(
    method='get',
    operation_summary="List All Cards",
    operation_description="Retrieve a list of all cards.",
    manual_parameters=[get_auth_header()],
    responses={200: CardSerializer(many=True)}
)
@api_view(['GET'])
def card_list(request):
    """Handles GET (list cards)"""
    if request.method == 'GET':
        cards = Card.objects.all()
        cards = cards.filter(user=request.user)
        cards = cards.filter(active=True)
        serializer = CardSerializer(cards, many=True)
        return Response(serializer.data)
    
