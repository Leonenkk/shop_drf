
from django.contrib.auth import get_user_model
from django.db import models
from apps.common.models import BaseModel
from phonenumber_field.modelfields import PhoneNumberField

class ShippingAddress(BaseModel):
    """
    Represents a shipping address associated with a user.

    Attributes:
        user (ForeignKey): The user who owns the shipping address.
        full_name (str): The full name of the recipient.
        email (EmailField): The email address of the recipient.
        phone (PhoneNumberField): The phone number of the recipient.
        address (str): The street address of the recipient.
        country (str): The country of the recipient.
        zipcode (str): The postal code of the recipient.
    Methods:
        __str__():
            Returns a string representation of the shipping details.
    """
    user=models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='shipping_address',
        verbose_name='Пользователь'
    )
    full_name=models.CharField(max_length=255,verbose_name='ФИО')
    email=models.EmailField(verbose_name='Адрес электронной почты')
    phone=PhoneNumberField(null=True,region='BY',verbose_name='Номер телефона')
    address=models.CharField(max_length=255,null=True,verbose_name='Адрес доставки')
    country=models.CharField(max_length=200,null=True,verbose_name='Страна доставки')
    zipcode=models.CharField(max_length=6,null=True,verbose_name='Почтовый индекс')

    def __str__(self):
        return f"{self.full_name}'s shipping details"



