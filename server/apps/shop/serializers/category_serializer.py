from apps.shop.models import Category
from rest_framework import serializers

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields=(
            'name',
            'slug',
            'image'
        )
        read_only_fields = ('slug',)