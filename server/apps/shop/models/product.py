from autoslug import AutoSlugField
from django.core.validators import FileExtensionValidator

from apps.common.models import IsDeletedModel, BaseModel
from django.db import models

from apps.sellers.models import Seller
from apps.shop.models import Category


class Product(IsDeletedModel):
    """
    Product model representing a product with seller and category details.

    Attributes:
        seller (ForeignKey): The seller associated with the product. Set to NULL if the seller is deleted.
        category (ForeignKey): The category to which the product belongs. Set to NULL if the category is deleted.
        name (str): The name of the product.
        slug (AutoSlugField): An automatically generated slug based on the product name, unique for each product.
        description (TextField): A description of the product.
        price_old (DecimalField): The old price of the product, can be NULL.
        price_current (DecimalField): The current price of the product.
        in_stock (PositiveIntegerField): The quantity of the product available in stock.

    Methods:
        __str__():
            Returns the name of the product as a string representation.
    """
    seller=models.ForeignKey(
        Seller,
        on_delete=models.SET_NULL,
        related_name='products',
        null=True,
        verbose_name='Продавец'
    )
    category=models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name='products',
        null=True,
        verbose_name='Категория товара'
    )
    name=models.CharField(max_length=100)
    slug=AutoSlugField(
        populate_from='name',
        unique=True,
        db_index=True,
        verbose_name='Slug'
    )
    description=models.TextField(blank=True,verbose_name='Описание товара')
    price_old=models.DecimalField(max_digits=10, decimal_places=2,null=True,verbose_name='Старая цена')
    price_current=models.DecimalField(max_digits=10, decimal_places=2,verbose_name='Текущая цена')
    in_stock=models.PositiveIntegerField(default=0,verbose_name='В продаже')

    def __str__(self):
        return self.name

def product_image_upload_to(instance, filename):
    return f'product_images/{instance.product.slug}/{filename}'

class ProductImages(BaseModel):
    """
    ProductImages model representing images associated with a product.
    Attributes:
        product (ForeignKey): The product to which the image is associated.
        image (ImageField): The image file of the product with valid extensions (png, jpg, jpeg, gif).
        order (PositiveIntegerField): The order in which the image should be displayed.
    Meta:
        ordering (list): Orders the images by the 'order' field.
    Methods:
        product_image_upload_to(instance, filename):
            Returns the upload path for the product image, using the product's slug.
    """
    product=models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='images',
        verbose_name='Продукт'
    )
    image=models.ImageField(
        upload_to=product_image_upload_to,
        validators=FileExtensionValidator(['png', 'jpg', 'jpeg', 'gif']),
        verbose_name='Фото товара'
    )
    order = models.PositiveIntegerField(default=0, verbose_name='Порядок')
    class Meta:
        ordering = ['order']