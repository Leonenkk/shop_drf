from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.profiles.models import OrderItem
from apps.shop.serializers import OrderItemSerializer


class CartView(APIView):
    serializer_class = OrderItemSerializer

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

    def post(self, request):
        serializer = self.serializer_class(data=request.data, user=request.user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def patch(self, request, *args, **kwargs):
        item = OrderItem.objects.get_or_none(
            product__slug=request.data["slug"],
            order=None,
            user=request.user,
        )
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

    def delete(self, request, *args, **kwargs):
        item = OrderItem.objects.get_or_none(
            product__slug=request.data["slug"],
            order=None,
            user=request.user,
        )
        if not item:
            return Response(
                {"detail": "Item not found"}, status=status.HTTP_404_NOT_FOUND
            )
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
