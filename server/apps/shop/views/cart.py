from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.profiles.models import OrderItem
from apps.shop.serializers.cart import OrderItemSerializer

tags = ["Cart"]


class CartView(APIView):
    serializer_class = OrderItemSerializer

    @extend_schema(
        operation_id="get_cart_item",
        summary="Get cart items",
        description="This method allows get cart items which not in order",
        tags=tags,
    )
    def get(self, request):
        user = request.user
        cart = OrderItem.objects.filter(user=user, order=None).select_related(
            "user",
            "order",
            "product",
            "product__seller",
        )
        serializer = self.serializer_class(cart, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        operation_id="add_item_in_cart",
        summary="Add item in cart",
        description="This method allows add item in cart",
        tags=tags,
    )
    def post(self, request):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CartDetailView(APIView):
    serializer_class = OrderItemSerializer

    def get_cart_item(self, user, slug):
        return OrderItem.objects.get_or_none(user=user, product__slug=slug, order=None)

    @extend_schema(
        operation_id="update_item_in_cart",
        summary="Update item in cart",
        description="""
            This method allows update product quantity in cart.
            If quantity is null,remove product from cart.
            """,
        tags=tags,
    )
    def patch(self, request, *args, **kwargs):
        item = self.get_cart_item(request.user, kwargs["slug"])
        if not item:
            return Response(
                {"detail": "Item not found"}, status=status.HTTP_404_NOT_FOUND
            )
        serializer = self.serializer_class(item, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        if serializer.validated_data["quantity"] == 0:
            item.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        operation_id="delete_item_from_cart",
        summary="Delete item in cart",
        description="This method allows delete item in cart",
        tags=tags,
    )
    def delete(self, request, *args, **kwargs):
        item = self.get_cart_item(request.user, kwargs["slug"])
        if not item:
            return Response(
                {"detail": "Item not found"}, status=status.HTTP_404_NOT_FOUND
            )
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# мб добавить get для конкретного товара в корзине для просмотра в CartDetailView, пока хз для чего
