from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from helpers.swagger import get_auth_header
from .models import Product
from .serialize import ProductSerializer


class ProductListView(APIView):
    """Handles listing and creating products"""

    @swagger_auto_schema(
        operation_summary="Get all products",
        manual_parameters=[get_auth_header()],
        responses={200: ProductSerializer(many=True)},
    )
    def get(self, _):
        """List all available products"""
        products = Product.objects.filter(is_available=True)
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary="Create a new product",
        operation_description="Create a new product with the provided data.",
        manual_parameters=[get_auth_header()],
        request_body=ProductSerializer,
        responses={201: ProductSerializer(), 400: "Invalid input"},
    )
    def post(self, request):
        """Create a new product"""
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductUpdateStockView(APIView):
    """Handles updating the stock of a product"""

    @swagger_auto_schema(
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
    def patch(self, request):
        """Update stock for a product"""
        try:
            product = Product.objects.get(id=request.data.get("id"))
        except Product.DoesNotExist:
            return Response(
                {"message": "Product not found"}, status=status.HTTP_404_NOT_FOUND
            )

        stock_update = request.data.get("stock")
        stock_update = int(stock_update) if stock_update is not None else None

        if stock_update is not None:
            product.stock = stock_update
            product.is_available = stock_update > 0
            product.save()
            return Response(ProductSerializer(product).data, status=status.HTTP_200_OK)

        return Response(
            {"message": "Stock value is required"}, status=status.HTTP_400_BAD_REQUEST
        )
