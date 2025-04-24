from django.utils import timezone
from apps.common.models import BaseModel
from apps.common.managers import IsDeletedManager
from django.db import models


class IsDeletedModel(BaseModel):
    """
    Model with soft and hard delete methods
    Attributes:
        is_deleted: bool
        deleted_at: datetime
    """
    is_deleted = models.BooleanField(default=False,verbose_name='Удалена')
    deleted_at = models.DateTimeField(blank=True,verbose_name='Удалена в')
    objects = IsDeletedManager()

    class Meta:
        abstract = True

    def delete(self, *args, **kwargs):
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save(update_fields=['is_deleted', 'deleted_at'])

    def hard_delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)
