from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Order, OrderItem
from .serializers import OrderSerializer
from cart.models import Cart


class OrderViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        # admin sees all orders, user sees only their own
        if request.user.role == 'ADMIN':
            orders = Order.objects.all()
        else:
            orders = Order.objects.filter(user=request.user)

        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)

    def checkout(self, request):
        try:
            cart = Cart.objects.get(user=request.user)
        except Cart.DoesNotExist:
            return Response(
                {'error': 'Cart not found'},
                status=status.HTTP_404_NOT_FOUND
            )

        if not cart.items.exists():
            return Response(
                {'error': 'Cart is empty'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # check stock before creating order
        for item in cart.items.all():
            if item.product.stock < item.quantity:
                return Response(
                    {'error': f'Not enough stock for {item.product.name}. Available: {item.product.stock}'},
                    status=status.HTTP_400_BAD_REQUEST
                )

        # create order
        order = Order.objects.create(user=request.user, status='PENDING')
        total = 0

        for item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity
            )
            # deduct stock
            item.product.stock -= item.quantity
            item.product.save()

            total += item.total_price()

        order.total = total
        order.save()

        # clear cart
        cart.items.all().delete()

        return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)