from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.common.permissions import IsSeller
from apps.shop.models import Product
from apps.shop.serializers import ProductCreateSerializer, ProductSerializer

tags = ["Sellers"]


class SellerProductView(APIView):
    serializer_class = ProductCreateSerializer
    permission_classes = (IsSeller,)

    @extend_schema(
        summary="Update product",
        description="""
        This method allows you to update an existing product for seller
        If current product belongs to seller and exists
        """,
        request=ProductCreateSerializer,
        responses=ProductSerializer,
        tags=tags,
    )
    def put(self, request, *args, **kwargs):
        product = get_object_or_404(Product, slug=self.kwargs["slug"])
        if product.seller != request.user.seller:
            return Response(
                {"message": "You do not have permission to edit this product."},
                status=status.HTTP_403_FORBIDDEN,
            )
        serializer = self.serializer_class(
            instance=product,
            data=request.data,
            partial=True,  # не забыть если что убрать и patch написать
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        summary="Delete product",
        description="""
        This method allows you to delete an existing product for seller
        """,
        tags=tags,
    )
    def delete(self, request, *args, **kwargs):
        product = get_object_or_404(Product, slug=kwargs["slug"])
        if product.seller != request.user.seller:
            return Response(
                {"message": "You do not have permission to edit this product."},
                status=status.HTTP_403_FORBIDDEN,
            )
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# patch запрос для частичного удаления, изменения порядка и добавления фото (add,remove,reorder)
