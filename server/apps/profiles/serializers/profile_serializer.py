from django.contrib.auth import get_user_model
from rest_framework import serializers


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model=get_user_model()
        fields=[
            'first_name',
            'last_name',
            'email',
            'avatar',
            'account_type'
        ]
        read_only_fields=['email','account_type']
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True},

        }