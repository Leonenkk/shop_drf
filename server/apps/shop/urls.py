from django.urls import path

from apps.shop.views import CategoryView

urlpatterns = [
    path('category/', CategoryView.as_view(), name='category'),
]