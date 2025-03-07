from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from helpers.swagger import get_auth_header
from .models import Product
from .serialize import ProductSerializer


@swagger_auto_schema(
    method="get",
    manual_parameters=[get_auth_header()],
    operation_summary="Get all products",
    responses={200: ProductSerializer(many=True)},
)
@api_view(["GET"])
def product_list(_):
    """List all products"""
    products = Product.objects.filter(is_available=True)  # Show only available products
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@swagger_auto_schema(
    method="post",
    operation_summary="Create a new product",
    operation_description="Create a new product with the provided data.",
    manual_parameters=[get_auth_header()],
    request_body=ProductSerializer,
    responses={201: ProductSerializer(), 400: "Invalid input"},
)
@api_view(["POST"])
def product_create(request):
    """Create a new product"""
    serializer = ProductSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(
    method="patch",
    operation_summary="Update a product",
    operation_description="Update a product with the provided data.",
    manual_parameters=[get_auth_header()],
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "id": openapi.Schema(type=openapi.TYPE_INTEGER),
            "stock": openapi.Schema(type=openapi.TYPE_INTEGER),
        },
    ),
    responses={200: ProductSerializer(), 400: "Invalid input"},
)
@api_view(["PATCH"])
def product_update_stock(request):
    """Update stock for a product"""
    try:
        product = Product.objects.get(id=request.data.get("id"))
    except Product.DoesNotExist:
        return Response(
            {"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND
        )

    stock_update = request.data.get("stock")
    stock_update = int(stock_update) if stock_update is not None else None

    if stock_update is not None:
        product.stock = stock_update
        product.is_available = stock_update > 0
        product.save()
        return Response(ProductSerializer(product).data, status=status.HTTP_200_OK)

    return Response(
        {"error": "Stock value is required"}, status=status.HTTP_400_BAD_REQUEST
    )
