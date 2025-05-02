from django.contrib import admin

from apps.sellers.models import Seller


@admin.register(Seller)
class SellerAdmin(admin.ModelAdmin):
    pass
