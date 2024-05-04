from django.contrib import admin
from django.urls import path, include

from vendor.views import vendors, vendor_performance, orders, acknowledge

urlpatterns = [
    path('vendors', vendors),
    path('vendors/<int:vendor_id>', vendors),
    path('vendors/<int:vendor_id>/performance', vendor_performance),
    path('purchase_orders', orders),
    path('purchase_orders/<int:po_id>', orders),
    path('purchase_orders/<int:po_id>/acknowledge', acknowledge),
]