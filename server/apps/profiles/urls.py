from django.urls import path

from apps.profiles.views import ProfileView
from apps.profiles.views import ShippingAddressViewID,ShippingAddressView

urlpatterns = [
    path('',ProfileView.as_view(), name='profile'),
    path('shipping_adresses/',ShippingAddressView.as_view(), name='shipping'),
    path('shipping_adresses/detail/<uuid:shipping_id>/',ShippingAddressViewID.as_view(), name='shipping_address'),
]

