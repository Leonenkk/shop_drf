from django.db import models
from django.utils import timezone
from apps.common.managers.get_or_none import GetOrNoneQuerySet, GetOrNoneManager


class IsDeletedQuerySet(GetOrNoneQuerySet):
    """Custom QuerySet for delete"""
    def delete(self,hard_delete=False):
        if hard_delete:
            return super().delete()
        else:
            return self.update(is_deleted=True,deleted_at=timezone.now())

class IsDeletedManager(GetOrNoneManager):
    """custom manager for hard and soft delete"""
    def get_queryset(self):
        return IsDeletedQuerySet(self.model, using=self._db).filter(is_deleted=False)

    def unfiltered(self):
        return IsDeletedQuerySet(self.model,using=self._db)

    def hard_delete(self):
        return self.unfiltered().delete(hard_delete=True)

    def deleted(self):
        return self.unfiltered().filter(is_deleted=True)