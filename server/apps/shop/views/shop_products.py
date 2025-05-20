from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.common.paginations import CustomPagination
from apps.sellers.models import Seller
from apps.shop.filters import ProductFilter
from apps.shop.models import Product
from apps.shop.schema_examples import PRODUCT_PARAM_EXAMPLES
from apps.shop.serializers import ProductSerializer

tags = ["Shop"]


class ProductDetailView(APIView):
    serializer_class = ProductSerializer

    @extend_schema(
        operation_id="product-detail",
        summary="Product Detail",
        description="""
        This method allows user get selected product details.
        """,
        tags=tags,
    )
    def get(self, request, *args, **kwargs):
        product = Product.objects.get_or_none(slug=self.kwargs["slug"])
        if not product:
            return Response(
                {"message": "Product does not exist"}, status=status.HTTP_404_NOT_FOUND
            )
        serializer = self.serializer_class(product)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProductsBySellerView(APIView):
    serializer_class = ProductSerializer

    @extend_schema(
        operation_id="products-by-seller",
        summary="Products By Seller",
        description="""
        This method allows user get all products by seller.
        """,
        tags=tags,
    )
    def get(self, request, *args, **kwargs):
        seller = Seller.objects.get_or_none(slug=self.kwargs["slug"])
        if not seller:
            return Response(
                {"message": "Shop does not exist"}, status=status.HTTP_404_NOT_FOUND
            )
        products = Product.objects.select_related(
            "category", "seller", "seller__user"
        ).filter(seller=seller)
        serializer = self.serializer_class(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProductsView(APIView):
    serializer_class = ProductSerializer
    pagination_class = CustomPagination

    @extend_schema(
        operation_id="products",
        summary="Products",
        description="""
        This method allows user get all products.
        """,
        tags=tags,
        parameters=PRODUCT_PARAM_EXAMPLES,
    )
    def get(self, request, *args, **kwargs):
        products = Product.objects.select_related(
            "category", "seller", "seller__user"
        ).all()
        filter_set = ProductFilter(request.query_params, queryset=products)
        if filter_set.is_valid():
            queryset = filter_set.qs
            paginator = self.pagination_class()
            paginated_queryset = paginator.paginate_queryset(queryset, request)
            serializer = self.serializer_class(paginated_queryset, many=True)
            return paginator.get_paginated_response(serializer.data)
        else:
            return Response(filter_set.errors, status=status.HTTP_400_BAD_REQUEST)
