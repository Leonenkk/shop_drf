from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.profiles.models import OrderItem, ShippingAddress, Order
from apps.shop.serializers.order import CheckoutSerializer, OrderSerializer

tags = ["Order"]


class CheckoutView(APIView):
    serializer_class = CheckoutSerializer

    @extend_schema(
        summary="Checkout",
        description="""
               This endpoint allows a user to create an order through which payment can then be made through.
               """,
        tags=tags,
        request=CheckoutSerializer,
    )
    def post(self, request, *args, **kwargs):
        user = request.user
        cart_items = OrderItem.objects.filter(user=user, order=None)
        if not cart_items.exists():
            return Response(
                {"message": "Cart is empty"}, status=status.HTTP_404_NOT_FOUND
            )
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        shipping_id = serializer.validated_data["shipping_id"]
        shipping = ShippingAddress.objects.get_or_none(id=shipping_id, user=user)
        if not shipping:
            return Response(
                {"message": " No shipping address with that ID"},
                status=status.HTTP_404_NOT_FOUND,
            )
        fields_to_update = (
            "full_name",
            "email",
            "phone",
            "address",
            "city",
            "country",
            "zipcode",
        )
        data = {}
        for field in fields_to_update:
            value = getattr(shipping, field)
            data[field] = value

        order = Order.objects.create(user=user, **data)
        cart_items.update(order=order)
        order_serializer = OrderSerializer(order)
        return Response(
            data={"message": "Checkout Successful", "item": order_serializer.data},
            status=status.HTTP_200_OK,
        )
