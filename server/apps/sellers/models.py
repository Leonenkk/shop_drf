from autoslug import AutoSlugField
from django.contrib.auth import get_user_model
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from apps.common.models import BaseModel


class Seller(BaseModel):
    """
    Seller model with business and bank details

    Attributes:
        user (ForeignKey): The user associated with the seller account.
        business_name (str): The name of the business or company.
        slug (AutoSlugField): An automatically generated slug based on the business name.
        inn_identification_number (str): The tax identification number (INN) for the business.
        website_url (URLField): The URL of the business website.
        phone_number (PhoneNumberField): The phone number of the business, validated for Belarus.
        business_description (TextField): A description of the business activities.
        business_address (str): The physical address of the business.
        city (str): The city where the business is located.
        zip_code (str): The postal code of the business location.
        bank_name (str): The name of the bank where the business holds an account.
        bank_bic_number (str): The Bank Identifier Code (BIC) of the bank.
        bank_account_number (str): The International Bank Account Number (IBAN) for the business.
        bank_routing_number (str): The bank routing number for the business account.
        is_approved (bool): A flag indicating whether the seller has been approved.

    Methods:
        __str__():
            Returns a string representation of the seller, including the business name.
    """
    user=models.OneToOneField(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='seller',
        verbose_name='Пользователь'
    )
    #business information
    business_name=models.CharField(max_length=255,verbose_name='Название компании')
    slug=AutoSlugField(
        populate_from='business_name',
        always_update=True,
        null=True,
        verbose_name='SLUG'
    )
    inn_identification_number=models.CharField(max_length=12,verbose_name='ИНН')#юр лицо-10
    website_url=models.URLField(null=True,verbose_name='URL-адрес сайта бизнеса',blank=True)
    phone_number=PhoneNumberField(region='BY', verbose_name='Номер телефона')
    business_description=models.TextField(null=True,verbose_name='Описание бизнеса')
    #address
    business_address=models.CharField(max_length=255,verbose_name='Адрес бизнеса')
    city=models.CharField(max_length=100,verbose_name='Город нахождения')
    zip_code=models.CharField(max_length=6,verbose_name='Почтовый индекс')
    #bank information
    bank_name=models.CharField(max_length=100,verbose_name='Название банка')
    bank_bic_number=models.CharField(max_length=9,verbose_name='BIC')
    bank_account_number=models.CharField(max_length=28,verbose_name='IBAN')
    bank_routing_number = models.CharField(max_length=20,verbose_name='Номер банковского счета ')

    is_approved=models.BooleanField(default=False,verbose_name='Проверен')

    def __str__(self):
        return f"Seller for {self.business_name}"



