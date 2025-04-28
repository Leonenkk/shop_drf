from rest_framework import serializers

from apps.profiles.models import ShippingAddress


class ShippingAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model=ShippingAddress
        fields=[
            'id',
            'full_name',
            'email',
            'phone',
            'address',
            'country',
            'zipcode',
            'city'
        ]
        read_only_fields=('id',)

    def create(self, validated_data):
        try:
            user = self.context['request'].user
            return ShippingAddress.objects.create(user=user, **validated_data)
        except Exception as e:
            raise serializers.ValidationError(f"Failed to create address: {str(e)}")