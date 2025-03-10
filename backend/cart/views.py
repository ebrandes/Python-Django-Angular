from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated


from addresses.models import Address
from cards.models import Card
from cart.serializer import CartSerializer
from .models import Cart, CartItem
from products.models import Product


class CartView(APIView):
    """Exibe o carrinho do usuário"""

    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Retorna o carrinho do usuário autenticado"""
        cart, created = Cart.objects.get_or_create(user=request.user)

        # ✅ Se o carrinho for criado agora, preenche address e payment_card automaticamente
        if created:
            cart.address = Address.objects.filter(user=request.user).first()
            cart.payment_card = Card.objects.filter(user=request.user).first()
            cart.save()

        serializer = CartSerializer(cart)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        """Define endereço e cartão para o carrinho"""
        cart, _ = Cart.objects.get_or_create(user=request.user)

        address = Address.objects.filter(user=request.user).first()
        payment_card = Card.objects.filter(user=request.user).first()

        # ✅ Atualiza o carrinho apenas se um novo endereço ou cartão for encontrado
        if address:
            cart.address = address
        if payment_card:
            cart.payment_card = payment_card

        cart.save()
        return Response(CartSerializer(cart).data, status=status.HTTP_200_OK)


class AddToCartView(APIView):
    """Adiciona produto ao carrinho"""

    permission_classes = [IsAuthenticated]

    def post(self, request):
        """Adiciona produto ao carrinho e preenche endereço/cartão se necessário"""
        cart, created = Cart.objects.get_or_create(user=request.user)

        # ✅ Se o carrinho acabou de ser criado, preenche address e payment_card automaticamente
        if created:
            cart.address = Address.objects.filter(user=request.user).first()
            cart.payment_card = Card.objects.filter(user=request.user).first()
            cart.save()

        product_id = request.data.get("product_id")
        quantity = int(request.data.get("quantity", 1))

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response(
                {"message": "Produto não encontrado"}, status=status.HTTP_404_NOT_FOUND
            )

        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        if created:
            cart_item.quantity = quantity
        else:
            cart_item.quantity += quantity

        cart_item.save()
        return Response(CartSerializer(cart).data, status=status.HTTP_200_OK)


class CheckoutView(APIView):
    """Finaliza a compra"""

    permission_classes = [IsAuthenticated]

    def post(self, request):
        """Finaliza o pedido e deduz estoque"""
        try:
            cart = Cart.objects.get(user=request.user)
        except Cart.DoesNotExist:
            return Response(
                {"message": "Carrinho não encontrado"}, status=status.HTTP_404_NOT_FOUND
            )

        if not cart.items.exists():  # type: ignore
            return Response(
                {"message": "O carrinho está vazio"}, status=status.HTTP_400_BAD_REQUEST
            )

        if not cart.address or not cart.payment_card:
            return Response(
                {"message": "Endereço e cartão são obrigatórios"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Deduzir estoque dos produtos
        for cart_item in cart.items.all():  # type: ignore
            if cart_item.product.stock < cart_item.quantity:
                return Response(
                    {"message": f"Estoque insuficiente para {cart_item.product.name}"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            cart_item.product.stock -= cart_item.quantity
            cart_item.product.save()

        # Limpa o carrinho
        cart.items.all().delete()  # type: ignore

        return Response(
            {"message": "Compra realizada com sucesso!"}, status=status.HTTP_200_OK
        )
