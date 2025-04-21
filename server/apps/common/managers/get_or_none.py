from django.db import models

class GetOrNoneQuerySet(models.QuerySet):
    """Custom QuerySet that supports get_or_none()"""
    def get_or_none(self,**kwargs):
        try:
            return self.get(**kwargs)
        except self.model.DoesNotExist:
            return None

#custom manager with get_or_none
GetOrNoneManager=models.Manager.from_queryset(GetOrNoneQuerySet)