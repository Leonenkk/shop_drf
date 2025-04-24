from django.contrib.auth import get_user_model
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from apps.common.models import BaseModel
from apps.common.utils import generate_unique_code

DELIVERY_STATUS_CHOICES = (
    ('PENDING','PENDING'),
    ('PACKING','PACKING'),
    ('SHIPPING','SHIPPING'),
    ('ARRIVING','ARRIVING'),
    ('SUCCESS','SUCCESS'),
)

PAYMENT_STATUS_CHOICES = (
    ('PENDING','PENDING'),
    ('PROCESSING','PROCESSING'),
    ('SUCCESSFUL','SUCCESSFUL'),
    ('CANCELED','CANCELED'),
    ('FAILED','FAILED'),
)
class Order(BaseModel):
    """
        Represents a customer's order.

        Attributes:
            user (ForeignKey): The user who placed the order.
            tx_ref (str): The unique transaction reference.
            delivery_status (str): The delivery status of the order.
            payment_status (str): The payment status of the order.
            date_delivered (datetime): The date the order was delivered.
        Methods:
            __str__():
                Returns a string representation of the transaction reference.
            save(*args, **kwargs):
                Overrides the save method to generate a unique transaction reference when a new order is created.
        """
    user=models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='orders',
        verbose_name='Пользователь'
    )
    tx_ref=models.CharField(
        max_length=100,
        unique=True,
        null=True,
        verbose_name='Уникальный код'
    )
    delivery_status=models.CharField(
        choices=DELIVERY_STATUS_CHOICES,
        max_length=8,
        default='PENDING',
        verbose_name='Статус доставки'
    )
    payment_status=models.CharField(
        choices=PAYMENT_STATUS_CHOICES,
        max_length=10,
        default='PENDING',
        verbose_name='Статус оплаты'
    )
    date_delivered=models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Дата доставки'
    )
    #ShippingAddress fields
    full_name=models.CharField(max_length=255,null=True)
    email=models.EmailField(null=True)
    phone=PhoneNumberField(null=True,region='BY')
    address=models.CharField(max_length=255,null=True)
    country=models.CharField(max_length=200,null=True)
    zipcode=models.CharField(max_length=6,null=True)

    def __str__(self):
        return self.delivery_status

    def save(self, *args, **kwargs):
        if not self.created_at:
            self.tx_ref=generate_unique_code(Order,"tx_ref")
        super(Order, self).save(*args, **kwargs)

