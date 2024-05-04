from django.contrib import admin
from django.urls import path, include

from vendor.views import vendors, vendor_performance

urlpatterns = [
    path('', vendors),
    path('<int:vendor_id>', vendors),
    path('<int:vendor_id>/performance', vendor_performance),
]