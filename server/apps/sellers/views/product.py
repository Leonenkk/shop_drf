from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.sellers.models import Seller
from apps.shop.models import Product
from apps.shop.serializers import ProductSerializer, ProductCreateSerializer

tags = ['Sellers']


class SellerProductsView(APIView):
    serializer_class = ProductSerializer

    @extend_schema(
        summary='Get seller products',
        description="""
        This method allows seller get all his products
        """,
        tags=tags
    )
    def get(self, request, *args, **kwargs):
        try:
            seller = request.user.seller
            if not seller.is_approved:
                raise PermissionDenied()
        except Seller.DoesNotExist:
            return Response(
                {
                'message': 'You do not have permission to view this product.'
            },status=status.HTTP_403_FORBIDDEN
        )
        products = Product.objects.select_related('category').prefetch_related('images').filter(seller=seller)
        serializer = self.serializer_class(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        summary='Create new product',
        description="""
        This method allows you to create a new product for seller
        If user is_approved and has status SELLER.
        """,
        request=ProductCreateSerializer,
        responses=ProductCreateSerializer,
        tags=tags
    )
    def post(self, request, *args, **kwargs):
        try:
            seller = request.user.seller
            if not seller.is_approved:
                raise PermissionDenied()
        except Seller.DoesNotExist:
            raise PermissionDenied("Seller profile not found")
        serializer = ProductCreateSerializer(
            data=request.data,
            context={
                'request': request,
                'seller': seller,
            }
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

