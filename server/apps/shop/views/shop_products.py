from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.sellers.models import Seller
from apps.shop.models import Product
from apps.shop.serializers import ProductSerializer

tags=['Shop']


class ProductDetailView(APIView):
    serializer_class = ProductSerializer

    @extend_schema(
        operation_id='product-detail',
        summary='Product Detail',
        description="""
        This method allows user get selected product details.
        """,
        tags=tags
    )
    def get(self, request, *args, **kwargs):
        product = Product.objects.get_or_none(slug=self.kwargs['slug'])
        if not product:
            return Response(
                {
                    'message': 'Product does not exist'
                }, status=status.HTTP_404_NOT_FOUND
            )
        serializer = self.serializer_class(product)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProductsBySellerView(APIView):
    serializer_class = ProductSerializer

    @extend_schema(
        operation_id='products-by-seller',
        summary='Products By Seller',
        description="""
        This method allows user get all products by seller.
        """,
        tags=tags
    )
    def get(self, request, *args, **kwargs):
        seller = Seller.objects.get_or_none(slug=self.kwargs['slug'])
        if not seller:
            return Response(
                {
                    'message': 'Shop does not exist'
                }, status=status.HTTP_404_NOT_FOUND
            )
        products = Product.objects.select_related('category', 'seller', 'seller__user').filter(seller=seller)
        serializer = self.serializer_class(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProductsView(APIView):
    serializer_class = ProductSerializer

    @extend_schema(
        operation_id='products',
        summary='Products',
        description="""
        This method allows user get all products.
        """,
        tags=tags
    )
    def get(self, request, *args, **kwargs):
        products = Product.objects.select_related('category', 'seller', 'seller__user').all()
        serializer = self.serializer_class(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
