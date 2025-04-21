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
        """manager returns not deleted objects by default"""
        return IsDeletedQuerySet(self.model, using=self._db).filter(is_deleted=False)

    def unfiltered(self):
        """give access for all objects(include deleted)"""
        return IsDeletedQuerySet(self.model,using=self._db)

    def hard_delete(self):
        """delete all objects-> MyModel.objects.hard_delete()"""
        return self.unfiltered().delete(hard_delete=True)

    def deleted(self):
        """view deleted objects"""
        return self.unfiltered().filter(is_deleted=True)