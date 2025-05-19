from django.urls import path

from apps.sellers.views import (
    SellersView,
    SellerProductsView,
    SellerProductView,
    SellerOrderItemsView,
    SellerOrderView,
)

urlpatterns = [
    path("", SellersView.as_view(), name="sellers"),
    path("products/", SellerProductsView.as_view(), name="products"),
    path("orders/", SellerOrderView.as_view(), name="orders"),
    path("orders/<str:tx_ref>/", SellerOrderItemsView.as_view(), name="orders_details"),
    path("products/<slug:slug>/", SellerProductView.as_view()),
]
