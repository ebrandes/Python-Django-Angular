from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from models import Cart, CartItem, Product
from serialize import CartSerializer


@api_view(["GET"])
def get_cart(request):
    """Retrieve the cart for the authenticated user"""
    cart = Cart.objects.get_or_create(user=request.user)
    serializer = CartSerializer(cart)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["POST"])
def add_to_cart(request):
    """Add product to cart"""
    cart, created = Cart.objects.get_or_create(user=request.user)
    product_id = request.data.get("product_id")
    quantity = request.data.get("quantity", 1)

    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return Response(
            {"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND
        )

    # Check stock availability
    if product.stock < quantity:
        return Response(
            {"error": "Not enough stock"}, status=status.HTTP_400_BAD_REQUEST
        )

    # Add or update CartItem
    cart_item = CartItem.objects.get_or_create(cart=cart, product=product)
    cart_item.quantity = quantity
    cart_item.save()

    return Response(CartSerializer(cart).data, status=status.HTTP_200_OK)


@api_view(["POST"])
def remove_from_cart(request):
    """Remove a product from the cart"""
    cart = Cart.objects.get(user=request.user)
    product_id = request.data.get("product_id")

    try:
        cart_item = CartItem.objects.get(cart=cart, product_id=product_id)
        cart_item.delete()
    except CartItem.DoesNotExist:
        return Response(
            {"error": "Product not in cart"}, status=status.HTTP_404_NOT_FOUND
        )

    return Response(CartSerializer(cart).data, status=status.HTTP_200_OK)


@api_view(["POST"])
def checkout(request):
    """Finalize purchase and reduce stock"""
    cart = Cart.objects.get(user=request.user)

    # Check if cart is empty
    if not cart.items.exists():
        return Response({"error": "Cart is empty"}, status=status.HTTP_400_BAD_REQUEST)

    # Validate stock
    for item in cart.items.all():
        if item.product.stock < item.quantity:
            return Response(
                {"error": f"Not enough stock for {item.product.name}"},
                status=status.HTTP_400_BAD_REQUEST,
            )

    # Deduct stock and process purchase
    for item in cart.items.all():
        item.product.stock -= item.quantity
        item.product.save()

    # Clear cart after successful purchase
    cart.clear_cart()

    return Response({"message": "Purchase successful!"}, status=status.HTTP_200_OK)
