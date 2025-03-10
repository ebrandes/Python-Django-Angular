from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from helpers.swagger import get_auth_header
from cards.serializer import CardSerializer
from .models import Card
from rest_framework import status


# Create your views here.
class CardsView(APIView):
    """Handles listing and creating products"""

    @swagger_auto_schema(
        operation_summary="Get all cards",
        manual_parameters=[get_auth_header()],
        responses={200: CardSerializer(many=True)},
    )
    def get(self, _):
        """List all available cards"""
        cards = Card.objects.all()
        serializer = CardSerializer(cards, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary="Create a new card",
        manual_parameters=[get_auth_header()],
        request_body=CardSerializer,
        responses={201: CardSerializer()},
    )
    def post(self, request):
        """Create a new card"""
        serializer = CardSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
