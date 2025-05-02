from django.urls import path

from apps.sellers.views import SellersView, ProductView

urlpatterns = [
    path('',SellersView.as_view(), name='sellers'),
    path('products/',ProductView.as_view(), name='products'),
]