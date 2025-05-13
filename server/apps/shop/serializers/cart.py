from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from apps.profiles.models import OrderItem
from apps.shop.models import Product
from apps.shop.serializers import SellerShopSerializer


class OrderItemProductSerializer(serializers.ModelSerializer):
    seller = SellerShopSerializer()

    class Meta:
        model = Product
        fields = ("seller", "name", "slug", "price_current")


class OrderItemSerializer(serializers.ModelSerializer):
    product = OrderItemProductSerializer(read_only=True)
    slug = serializers.CharField(required=True, write_only=True)
    total_price_field = serializers.SerializerMethodField()

    class Meta:
        model = OrderItem
        fields = ("quantity", "product", "total_price_field", "slug")
        extra_kwargs = {"user": {"write_only": True}}

    def validate_slug(self, value):
        if not Product.objects.filter(slug=value).exists():
            raise serializers.ValidationError(
                {"slug": f"Product with slug {value} not found"}
            )
        return value

    def create(self, validated_data):
        slug = validated_data.pop("slug")
        product = Product.objects.get(slug=slug)
        validated_data["product"] = product
        user = self.context["request"].user
        if validated_data["quantity"] < 0:
            raise serializers.ValidationError({"quantity": "must be positive"})
        existing = OrderItem.objects.filter(
            product=product, user=user, order=None
        ).first()
        if existing:
            existing.quantity += validated_data["quantity"]
            if existing.quantity > product.in_stock:
                raise serializers.ValidationError(
                    {
                        "quantity": f"Not enough in stock. Items in stock {product.in_stock}"
                    }
                )
            existing.save()
            return existing
        validated_data["user"] = user
        if product.in_stock < validated_data["quantity"]:
            raise serializers.ValidationError(
                {"quantity": f"Not enough in stock. Items in stock {product.in_stock}"}
            )
        return super().create(validated_data)

    def update(self, instance, validated_data):
        if "quantity" in validated_data:
            if instance.product.in_stock < validated_data["quantity"]:
                raise serializers.ValidationError({"quantity": "Not enough in stock"})
        return super().update(instance, validated_data)

    @extend_schema_field(serializers.DecimalField(max_digits=10, decimal_places=2))
    def get_total_price_field(self, obj):
        return obj.get_total_price
