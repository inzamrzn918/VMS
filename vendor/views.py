import datetime
import json
import traceback

from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.utils import timezone
from rest_framework.decorators import api_view
from rest_framework.exceptions import NotFound

from vendor.models import Vendor, HistoricalPerformance, PurchaseOrder
from vendor.serializers import VendorSerializer, VendorPerformance, PurchaseOrderSerializer


# Create your views here.


@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def vendors(request, vendor_id=None):
    response = {"status_code": 500}
    try:
        if request.method == 'GET':
            if vendor_id is None:
                vendors = Vendor.objects.all()
                response['extra'] = VendorSerializer(vendors, many=True).data
            else:
                vendor = Vendor.objects.get(pk=vendor_id)
                if not vendor:
                    raise NotFound(
                        "Vendor not found with the ID"
                    )
                response['extra'] = VendorSerializer(vendor).data
        elif request.method == 'POST':
            json_data = json.loads(request.body)
            json_data["on_time_delivery_rate"] = 0
            json_data["quality_rating_avg"] = 0
            json_data["fulfillment_rate"] = 0
            json_data["average_response_time"] = 0
            vendor = Vendor(**json_data, )
            vendor.save()
            response['status_code'] = 201
            response['message'] = "Vendor Created"
        elif request.method == 'PUT':
            json_data = json.loads(request.body)
            vendor = Vendor.objects.get(pk=vendor_id)
            if not vendor:
                raise NotFound(
                    "Vendor not found with the ID"
                )
            for k, v in json_data.items():
                setattr(vendor, k, v)
            vendor.save()
            response['status_code'] = 201
            response['message'] = "Vendor Created"
        elif request.method == 'DELETE':
            vendor = Vendor.objects.get(pk=vendor_id)
            if not vendor:
                raise NotFound(
                    "Vendor not found with the ID"
                )
            vendor.delete()
            response['status_code'] = 200
            response['message'] = "Deleted"

        return JsonResponse(response)
    except Exception as e:
        response['traceback'] = str(e)
        return JsonResponse(response)


def vendor_performance(request, vendor_id):
    response = {"status_code": 200}
    try:
        performances = HistoricalPerformance.objects.filter(vendor_id=vendor_id).all()

        if not performances:
            raise NotFound(f"No historical performance data found for vendor with ID {vendor_id}")

        # Serialize the historical performance data
        serializer = VendorPerformance(performances, many=True)
        data = serializer.data
        nd = {}
        for d in data:
            for key, value in d.items():
                if key in nd:
                    nd[key] += value
                else:
                    nd[key] = value

        average_values = {key: sum_value / len(data) for key, sum_value in nd.items()}

        response['data'] = average_values
    except Exception as e:
        traceback.print_exc()
        response['traceback'] = str(e)
    return JsonResponse(response)


@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def orders(request, po_id=None):
    response = {"status_code": 500}
    try:
        if request.method == 'GET':
            if po_id is None:
                pos = PurchaseOrder.objects.all()
                response['extra'] = PurchaseOrderSerializer(pos, many=True).data
            else:
                po = PurchaseOrder.objects.get(pk=po_id)
                response['extra'] = PurchaseOrderSerializer(po).data
        elif request.method == 'POST':
            json_data = json.loads(request.body)
            vendor = Vendor.objects.get(pk=json_data['vendor_id'])
            if not vendor:
                raise NotFound(
                    "Vendor not found with the ID"
                )
            po = PurchaseOrder(vendor=vendor, order_date=datetime.datetime.now(datetime.timezone.utc),
                               delivery_date=datetime.datetime.now(datetime.timezone.utc), items=json.dumps({}),
                               quantity=1, status='completed', quality_rating=5,
                               issue_date=datetime.datetime.now(datetime.timezone.utc))
            po.save()
            response['status_code'] = 201
            response['message'] = "Order Created"
        elif request.method == 'PUT':
            json_data = json.loads(request.body)
            po = PurchaseOrder.objects.get(pk=po_id)
            for k, v in json_data.items():
                setattr(po, k, v)
            po.save()
            response['status_code'] = 201
            response['message'] = "Order Created"
        elif request.method == 'DELETE':
            po = PurchaseOrder.objects.get(pk=po_id)
            if not po:
                raise NotFound(
                    "Vendor not found with the ID"
                )
            po.delete()
            response['status_code'] = 200
            response['message'] = "Deleted"

    except Exception as e:
        response['traceback'] = str(e)
    return JsonResponse(response)


@api_view(['POST'])
def acknowledge(request, po_id):
    response = {"status_code": 500}
    try:
        # pos = PurchaseOrder.objects.get(pk=po_id)
        # if not pos:
        #     raise NotFound(
        #         "PurchaseOrder not found with the ID"
        #     )
        try:
            purchase_order = PurchaseOrder.objects.get(pk=po_id)
        except ObjectDoesNotExist:
            raise NotFound(f"PurchaseOrder not found with ID: {po_id}")

            # Update the acknowledgment_date to the current time
        purchase_order.acknowledgment_date = timezone.now()
        purchase_order.save()
        response['status_code'] = 202
        response['message'] = "Acknowledgement Received"
    except Exception as e:
        traceback.print_exc()
        response['traceback'] = str(e)
    return JsonResponse(response)
