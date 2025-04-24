import uuid
from apps.common.managers import GetOrNoneManager
from django.db import models

class BaseModel(models.Model):
    """base model with common fields
    Attributes:
        id (UUIDField): Unique identifier for the model instance.
        created_at (DateTimeField): Timestamp when the instance was created.
        updated_at (DateTimeField): Timestamp when the instance was last updated.
    """

    id=models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)#editable-block editing
    created_at=models.DateTimeField(auto_now_add=True,verbose_name='Создана в')
    updated_at=models.DateTimeField(auto_now=True, verbose_name='Обновлена в ')
    objects=GetOrNoneManager()
    class Meta:
        abstract = True