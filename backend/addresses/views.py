from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from addresses.serializer import AddressSerializer
from helpers.swagger import get_auth_header
from .models import Address
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


@swagger_auto_schema(
    method="POST",
    operation_summary="Create Address",
    operation_description="Create a new address for the authenticated user.",
    manual_parameters=[get_auth_header()],
    request_body=AddressSerializer,
    responses={201: "Address created successfully", 401: "User not authenticated"},
)
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_address(request):
    """
    Create a new address for the authenticated user.
    """
    user = request.user

    if not user:
        return Response(
            {"message": "User not authenticated"}, status=status.HTTP_401_UNAUTHORIZED
        )

    address = AddressSerializer(data=request.data)
    if address.is_valid():
        address = address.save(user=user)

    return Response(
        {"message": "Address created successfully", "address_id": address.id},
        status=status.HTTP_201_CREATED,
    )


@swagger_auto_schema(
    method="GET",
    operation_summary="Get Addresses",
    operation_description="Get List of Addresses.",
    manual_parameters=[get_auth_header()],
    responses={200: AddressSerializer()},
)
@api_view(["GET"])
def get_addresses(request):
    """
    List all addresses for the authenticated user.
    """
    user = request.user

    if not user:
        return Response(
            {"message": "User not authenticated"}, status=status.HTTP_401_UNAUTHORIZED
        )

    addresses = Address.objects.filter(user=user)
    serializer = AddressSerializer(addresses, many=True)
    return Response(serializer.data)


@swagger_auto_schema(
    method="PATCH",
    operation_summary="Select Address as Default",
    operation_description="Select an address as default for the authenticated user.",
    manual_parameters=[get_auth_header()],
    request_body=AddressSerializer,
    responses={200: "Address selected as default", 401: "User not authenticated"},
)
@api_view(["PATCH"])
def patch_address(request):
    """
    Select an address as default for the authenticated user.
    """
    user = request.user

    if not user or not user.is_authenticated:
        return Response(
            {"message": "User not authenticated"}, status=status.HTTP_401_UNAUTHORIZED
        )

    # Obtém o ID do endereço a ser atualizado
    address_id = request.data.get("id")
    if not address_id:
        return Response(
            {"message": "Address ID is required"}, status=status.HTTP_400_BAD_REQUEST
        )

    # Busca o endereço do usuário
    try:
        address = Address.objects.get(id=address_id, user=user)
    except Address.DoesNotExist:
        return Response(
            {"message": "Address not found"}, status=status.HTTP_404_NOT_FOUND
        )

    # Atualiza apenas os campos enviados no request
    serializer = AddressSerializer(
        address, data=request.data, partial=True
    )  # ✅ Atualiza sem criar um novo objeto
    if serializer.is_valid():
        serializer.save()  # ✅ Apenas os campos enviados são alterados
        return Response(serializer.data, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
