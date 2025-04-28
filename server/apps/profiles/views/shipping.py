from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.profiles.models import ShippingAddress
from apps.profiles.serializers import ShippingAddressSerializer

tags=['Profiles']

class ShippingAddressView(APIView):
    serializer_class = ShippingAddressSerializer

    @extend_schema(
        summary="Shipping Addresses Fetch",
        description="""
            This endpoint returns all shipping addresses associated with a user.
        """,
        tags=tags,
    )
    def get(self, request):
        user=request.user
        shipping_addresses=ShippingAddress.objects.select_related('user').filter(user=user)
        serializer=self.serializer_class(shipping_addresses, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        summary='Create Shipping Addresses',
        description="""
        This endpoint creates a new shipping address associated with a user.
        """,
        tags=tags,
    )
    def post(self, request):
        serializer=self.serializer_class(
            data=request.data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

