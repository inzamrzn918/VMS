from django.contrib import admin
from django.urls import path, include

from po.views import orders, acknowledge

urlpatterns = [
    path('', orders),
    path('<int:po_id>', orders),
    path('<int:po_id>/acknowledge', acknowledge),
]