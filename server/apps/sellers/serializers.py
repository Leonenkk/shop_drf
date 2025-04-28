from rest_framework import serializers
from apps.sellers.models import Seller

class SellerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seller
        fields = (
            'business_name',
            'slug',
            'inn_identification_number',
            'website_url',
            'phone_number',
            'business_description',
            'business_address',
            'city',
            'zip_code',
            'bank_name',
            'bank_bic_number',
            'bank_account_number',
            'bank_routing_number',
            'is_approved'
        )
        read_only_fields = ('slug','is_approved')
        #мб убрать(избыточно)
        extra_kwargs = {
            'website_url': {'required': False},
        }