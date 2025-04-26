from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from django.core.exceptions import ValidationError
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, AuthUser
from rest_framework_simplejwt.tokens import Token


class CreateUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        validators=[validate_password]
    )
    class Meta:
        model=get_user_model()
        fields=['email','password']

    def create(self,validated_data):
        user=super(CreateUserSerializer,self).create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user: AuthUser) -> Token:
        token=super(MyTokenObtainPairSerializer,cls).get_token(user)
        if user.is_staff:
            token['group']='admin'
        else:
            token['group']='user'
            token['role']=user.account_type
        return token