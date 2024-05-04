from rest_framework.serializers import ModelSerializer

from vendor.models import Vendor, PurchaseOrder, HistoricalPerformance


class VendorSerializer(ModelSerializer):
    class Meta:
        model = Vendor
        fields = '__all__'


class PurchaseOrderSerializer(ModelSerializer):
    class Meta:
        model = PurchaseOrder
        fields = '__all__'


class HistoricalPerformanceSerializer(ModelSerializer):
    class Meta:
        model = HistoricalPerformance
        fields = '__all__'


class VendorPerformance(ModelSerializer):
    class Meta:
        model = Vendor
        fields = ['on_time_delivery_rate', 'average_response_time', 'fulfillment_rate', 'quality_rating_avg']
