from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.response import Response

from apps.shop.models import Category
from apps.shop.serializers import CategorySerializer
from rest_framework.views import APIView

tags=['Shop']

class CategoryView(APIView):
    serializer_class = CategorySerializer
    @extend_schema(
        summary="Categories Fetch",
        description="""
                This endpoint returns all categories.
            """,
        tags=tags
    )
    def get(self, request):
        categories = Category.objects.all()
        serializer = self.serializer_class(categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    @extend_schema(
        summary="Category Creating",
        description="""
            This endpoint creates categories.
        """,
        tags=tags
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
