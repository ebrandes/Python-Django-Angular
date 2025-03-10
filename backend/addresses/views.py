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

    if not user:
        return Response(
            {"message": "User not authenticated"}, status=status.HTTP_401_UNAUTHORIZED
        )

    addresses = Address.objects.filter(user=user)
    for address in addresses:
        address.selected = False
        address.save()

    address_id = request.data.get("id")
    address = Address.objects.get(id=address_id)
    address.selected = True
    address.save()

    return Response(
        {"message": "Address selected as default"}, status=status.HTTP_200_OK
    )
