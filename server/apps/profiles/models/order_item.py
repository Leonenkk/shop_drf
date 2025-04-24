from django.contrib.auth import get_user_model
from django.db import models
from apps.common.models import BaseModel
from apps.profiles.models.order import Order
from apps.shop.models import Product


class OrderItem(BaseModel):
    """
    Represents an item within an order.

    Attributes:
        user (ForeignKey):  The order to which this item belongs.
        order (ForeignKey): The order to which this item belongs.
        product (ForeignKey): The product associated with this order item.
        quantity (int): The quantity of the product ordered.
    Methods:
        __str__():
            Returns a string representation of the transaction reference.
        get_total_price()
            Return item total price
    """
    user=models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='order_items',
        blank=True,
        null=True
    )
    order=models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='order_items',
        blank=True,
        null=True
    )
    product=models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='order_items',
    )
    quantity=models.PositiveIntegerField(default=1)

    @property
    def get_total_price(self):
        return self.product.price_current * self.quantity

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return self.product.name