import datetime
import uuid

from django.db import models
from django.db.models import Avg
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone


class Vendor(models.Model):
    name = models.CharField(max_length=255)
    contact_details = models.TextField()
    address = models.TextField()
    vendor_code = models.UUIDField(max_length=100, default=uuid.uuid4(), unique=True)
    on_time_delivery_rate = models.FloatField()
    quality_rating_avg = models.FloatField()
    average_response_time = models.FloatField()
    fulfillment_rate = models.FloatField()

    def __str__(self):
        return self.name


class PurchaseOrder(models.Model):
    po_number = models.UUIDField(max_length=100, default=uuid.uuid4(), unique=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    order_date = models.DateTimeField()
    delivery_date = models.DateTimeField()
    items = models.JSONField()
    quantity = models.IntegerField()
    status = models.CharField(max_length=100)
    quality_rating = models.FloatField(null=True, blank=True)
    issue_date = models.DateTimeField()
    acknowledgment_date = models.DateTimeField(null=True)

    def __str__(self):
        return self.vendor.name


class HistoricalPerformance(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)
    on_time_delivery_rate = models.FloatField()
    quality_rating_avg = models.FloatField()
    average_response_time = models.FloatField()
    fulfillment_rate = models.FloatField()

    def __str__(self):
        return f"{self.vendor.name} - {self.date}"


@receiver(post_save, sender=PurchaseOrder)
def calculate_on_time_delivery_rate(sender, instance, created, **kwargs):
    if instance.status == 'completed':
        vendor = instance.vendor
        completed_pos = PurchaseOrder.objects.filter(vendor=vendor, status='completed')
        on_time_delivered_pos = completed_pos.filter(delivery_date__lte=datetime.datetime.now(datetime.timezone.utc))
        total_completed_pos = completed_pos.count()

        hd = HistoricalPerformance()
        hd.vendor = vendor

        if total_completed_pos > 0:
            on_time_delivery_rate = on_time_delivered_pos.count() / total_completed_pos * 100
            quality_rating_sum = completed_pos.aggregate(models.Avg('quality_rating'))[
                'quality_rating__avg']

            hd.quality_rating_avg = quality_rating_sum
            hd.on_time_delivery_rate = on_time_delivery_rate
            vendor.on_time_delivery_rate = on_time_delivery_rate
            vendor.quality_rating_avg = quality_rating_sum

            # response_times = completed_pos.exclude(acknowledgment_date__isnull=True).annotate(
            #     response_time=models.F('acknowledgment_date') - models.F(''
            #                                                              ''
            #                                                              '')).aggregate(
            #     avg_response_time=Avg('response_time'))['avg_response_time'] or 0
            response_times = completed_pos.exclude(acknowledgment_date__isnull=True).annotate(
                response_time=models.F('acknowledgment_date') - models.F('issue_date')
            ).aggregate(avg_response_time=Avg('response_time'))['avg_response_time'] or 0
            hd.average_response_time = response_times.total_seconds() / 3600 if response_times != 0 else response_times
            hd.fulfillment_rate = (completed_pos.count() / total_completed_pos) * 100
            vendor.average_response_time = hd.average_response_time
            vendor.fulfillment_rate = hd.fulfillment_rate
            hd.save()
