from django.db import models

class GetOrNoneQuerySet(models.QuerySet):
    """Custom QuerySet that supports get_or_none()"""
    def get_or_none(self,**kwargs):
        try:
            return self.get(**kwargs)
        except self.model.DoesNotExist:
            return None

class GetOrNoneManager(models.Manager):
    """Adds get_or_none method to objects"""
    def get_query_set(self):
        return GetOrNoneQuerySet(self.model)

    def get_or_none(self,**kwargs):
        return GetOrNoneQuerySet(self.model).get_or_none(**kwargs)