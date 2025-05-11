from rest_framework import serializers

from apps.profiles.models import OrderItem
from apps.sellers.serializers import SellerSerializer
from apps.shop.models import Product


class OrderItemProductSerializer(serializers.ModelSerializer):
    seller = SellerSerializer()

    class Meta:
        model = Product
        fields = ("seller", "name", "slug", "price_current")


class OrderItemSerializer(serializers.ModelSerializer):
    product = OrderItemProductSerializer()
    slug = serializers.SlugRelatedField(
        source="product", slug_field="slug", queryset=Product.objects.all()
    )  # аналог-SlugField + валидация в Create и Update, дает нам больше контроля

    class Meta:
        model = OrderItem
        fields = ("quantity", "product", "get_total_price", "slug", "user")
