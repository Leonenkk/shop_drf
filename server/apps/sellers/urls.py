from django.urls import path

from apps.sellers.views import SellersView, SellerProductsView, SellerProductView

urlpatterns = [
    path('',SellersView.as_view(), name='sellers'),
    path('products/', SellerProductsView.as_view(), name='products'),
    path('products/<slug:slug>/', SellerProductView.as_view()),
]