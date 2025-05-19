from django.urls import path

from apps.shop.views import (
    CategoryView,
    ProductByCategoryView,
    ProductsView,
    ProductDetailView,
    ProductsBySellerView,
    CheckoutView,
    CartView,
    CartDetailView,
    OrdersView,
    OrderItemView,
)

urlpatterns = [
    path("categories/", CategoryView.as_view(), name="category"),
    path("products/", ProductsView.as_view(), name="products"),
    path("checkout/", CheckoutView.as_view(), name="checkout"),
    path("cart/", CartView.as_view(), name="cart-list"),
    path("orders/", OrdersView.as_view(), name="orders"),
    path("orders/<str:tx_ref>/", OrderItemView.as_view(), name="order-item"),
    path("cart/<slug:slug>/", CartDetailView.as_view(), name="cart-detail"),
    path(
        "sellers/<slug:slug>/", ProductsBySellerView.as_view(), name="seller-products"
    ),
    path("products/<slug:slug>/", ProductDetailView.as_view(), name="product-detail"),
    path("categories/<slug:slug>/", ProductByCategoryView.as_view(), name="category"),
]
