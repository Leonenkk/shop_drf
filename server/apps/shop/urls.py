from django.urls import path
from apps.shop.views import CategoryView,ProductByCategoryView,ProductsView,ProductDetailView,ProductsBySellerView

urlpatterns = [
    path('categories/', CategoryView.as_view(), name='category'),
    path('products/',ProductsView.as_view(), name='products'),
    path('sellers/<slug:slug>/', ProductsBySellerView.as_view(), name='seller-products'),
    path('products/<slug:slug>/', ProductDetailView.as_view(), name='product-detail'),
    path('categories/<slug:slug>/', ProductByCategoryView.as_view(), name='category'),
]