from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.common.permissions import IsOwner
from apps.profiles.models import ShippingAddress
from apps.profiles.serializers import ShippingAddressSerializer

tags = ["Profiles"]


class ShippingAddressViewID(APIView):
    serializer_class = ShippingAddressSerializer
    permission_classes = (IsOwner,)

    def get_object(self, user, shipping_id):
        shipping_address = ShippingAddress.objects.get_or_none(id=shipping_id)
        if shipping_address:
            self.check_object_permissions(self.request, shipping_address)
        return shipping_address

    @extend_schema(
        summary="Get Shipping Address",
        description="""
        This endpoint returns a single shipping address associated with a user.
        """,
        tags=tags,
    )
    def get(self, request, shipping_id):
        shipping_address = self.get_object(request.user, shipping_id)
        if not shipping_address:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = self.serializer_class(shipping_address)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        summary="Update Shipping Address",
        description="""
        This endpoint updates a single shipping address associated with a user.
        """,
        tags=tags,
    )
    def put(self, request, shipping_id):
        shipping_address = self.get_object(request.user, shipping_id)
        if not shipping_address:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = self.serializer_class(
            shipping_address,
            data=request.data,
            context={"request": request},
            partial=True,  # не забыть если что убрать, либо доп метод
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        summary="Delete Shipping Address",
        description="""
        This endpoint deletes a single shipping address associated with a user.
        """,
        tags=tags,
    )
    def delete(self, request, shipping_id):
        shipping_address = self.get_object(request.user, shipping_id)
        if not shipping_address:
            return Response(status=status.HTTP_404_NOT_FOUND)
        shipping_address.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
