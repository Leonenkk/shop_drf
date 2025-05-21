from django.contrib.auth import get_user_model
from django.db import models

from apps.common.models import IsDeletedModel
from apps.shop.models import Product

RATING_CHOICES = (
    (1, 1),
    (2, 2),
    (3, 3),
    (4, 4),
    (5, 5),
)


class Review(IsDeletedModel):
    user = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name="reviewer"
    )
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="reviews"
    )
    rating = models.PositiveIntegerField(choices=RATING_CHOICES, default=1)
    text = models.TextField()
