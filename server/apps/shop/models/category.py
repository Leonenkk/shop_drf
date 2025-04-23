from autoslug import AutoSlugField
from django.core.validators import FileExtensionValidator

from apps.common.models import BaseModel
from django.db import models

class Category(BaseModel):
    """
    Represents a product category.
    Attributes:
        name (str): The category name, unique for each instance.
        slug (str): The slug generated from the name, used in URLs.
        image (ImageField): An image representing the category.

    Methods:
        __str__():
            Returns the string representation of the category name.
    """
    name=models.CharField(max_length=100,verbose_name='Название категории')
    slug=AutoSlugField(populate_from='name',verbose_name='Slug')
    image=models.ImageField(
        upload_to='category_images/',
        validators=FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png']),
        verbose_name='Фото категории',
        blank=True,
    )

    def __str__(self):
        return self.name