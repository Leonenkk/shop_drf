from django.core.validators import MinValueValidator
from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from apps.profiles.serializers import ShippingAddressSerializer


class CheckoutSerializer(serializers.Serializer):
    shipping_id = serializers.UUIDField()


class OrderSerializer(serializers.Serializer):
    tx_ref = serializers.CharField()
    first_name = serializers.CharField(source="user.first_name")
    last_name = serializers.CharField(source="user.last_name")
    email = serializers.EmailField(source="user.email")
    delivery_status = serializers.CharField()
    payment_status = serializers.CharField()
    date_delivered = serializers.DateTimeField()
    shipping_details = serializers.SerializerMethodField()
    subtotal = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        source="get_cart_subtotal",
        validators=[MinValueValidator(0.0)],
    )
    total = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        source="get_cart_total",
        validators=[MinValueValidator(0.0)],
    )

    @extend_schema_field(ShippingAddressSerializer)
    def get_shipping_details(self, obj):
        return ShippingAddressSerializer(obj).data
