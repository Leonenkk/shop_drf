from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.sellers.models import Seller
from apps.sellers.serializers import SellerSerializer

tags = ['Sellers']


class SellersView(APIView):
    serializer_class = SellerSerializer

    @extend_schema(
        summary="Apply to become a seller",
        description="""
            This endpoint allows a buyer to apply to become a seller.
        """,
        tags=tags
    )
    def post(self, request):
        user = request.user
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        seller, _ = Seller.objects.update_or_create(user=user, defaults=serializer.validated_data)
        user.account_type = 'SELLER'
        user.save()
        out_serializer = self.serializer_class(seller)
        return Response(out_serializer.data, status=status.HTTP_201_CREATED)

    @extend_schema(
        summary='Get seller details',
        description="""
        This endpoint allows to get seller details.
        """,
        tags=tags
    )
    def get(self, request):
        user = request.user
        seller = Seller.objects.select_related('user').filter(user=user)
        serializer = self.serializer_class(seller, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)






