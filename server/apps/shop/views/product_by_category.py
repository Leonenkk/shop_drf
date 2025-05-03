from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.shop.models import Category, Product
from apps.shop.serializers import ProductSerializer

tags=['Shop']
class ProductByCategoryView(APIView):
    serializer_class = ProductSerializer

    @extend_schema(
        operation_id='get_products_by_category',
        summary='Get products by category',
        description='This method allows you to get all products by category.',
        tags=tags,
    )
    def get(self, request,*args,**kwargs):
        category=Category.objects.get_or_none(slug=self.kwargs['slug'])
        if not category:
            return Response(
                {
                    'message': 'category not found',
                },status=status.HTTP_404_NOT_FOUND
            )
        products=Product.objects.select_related('category','seller','seller__user').filter(category=category)
        serializer = self.serializer_class(products, many=True)
        return Response(serializer.data)

