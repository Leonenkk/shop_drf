from django.contrib.auth.base_user import BaseUserManager
from django.core.validators import validate_email
from rest_framework.exceptions import ValidationError


class CustomUserManager(BaseUserManager):

    def validate_email(self,email):
        try:
            validate_email(email)
        except ValidationError:
            raise ValidationError('Email address is not valid')

    def validate_user(self,first_name,last_name,email,password):
        if not first_name:
            raise ValidationError('First name is required')
        if not last_name:
            raise ValidationError('Last name is required')
        if not email:
            raise ValidationError('Email address is required')
        email = self.normalize_email(email)
        self.validate_email(email)
        if not password:
            raise ValidationError('Password is required')

    def prepare_superuser_fields(self,**extra_fields):
        extra_fields.setdefault('is_superuser',True)
        extra_fields.setdefault('is_staff',True)
        if extra_fields.get('is_staff') is not True:
            raise ValidationError('Superuser must have is_staff=True')
        return extra_fields

    def create_user(self, first_name, last_name, email, password,**extra_fields):
        self.validate_user(first_name,last_name,email,password)
        user=self.model(
            first_name=first_name,
            last_name=last_name,
            email=email,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self,first_name,last_name,email,password,**extra_fields):
        extra_fields=self.prepare_superuser_fields(**extra_fields)
        return self.create_user(first_name,last_name,email,password,**extra_fields)

