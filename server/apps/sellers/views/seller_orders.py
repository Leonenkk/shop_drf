from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.profiles.models import Order, OrderItem
from apps.shop.serializers.order import OrderSerializer, CheckItemOrderSerializer

tags = ["Sellers"]


class SellerOrderView(APIView):

    serializer_class = OrderSerializer

    @extend_schema(
        summary="Seller orders",
        description="This method returns all orders that have like one seller item in it",
        tags=tags,
        operation_id="seller-orders",
    )
    def get(self, request):
        seller = request.user.seller
        orders = Order.objects.filter(order_items__product__seller=seller).order_by(
            "created_at"
        )
        serializer = self.serializer_class(orders, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class SellerOrderItemsView(APIView):

    serializer_class = CheckItemOrderSerializer

    @extend_schema(
        summary="List of order items",
        description="This method return List of order items belonging to this seller",
        tags=tags,
        operation_id="seller-orders-items",
    )
    def get(self, request, *args, **kwargs):
        seller = request.user.seller
        order = Order.objects.get_or_none(tx_ref=self.kwargs["tx_ref"])
        if not order:
            return Response(
                {"message": "Order not found"}, status=status.HTTP_404_NOT_FOUND
            )
        order_items = OrderItem.objects.filter(order=order, product__seller=seller)
        serializer = self.serializer_class(order_items, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
