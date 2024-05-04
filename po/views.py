import datetime
import datetime
import json
import traceback

from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.template.backends import django
from rest_framework.decorators import api_view
from rest_framework.exceptions import NotFound

from vendor.models import Vendor, PurchaseOrder
from vendor.serializers import PurchaseOrderSerializer
from django.utils import timezone

# Create your views here.


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
            # Handle DELETE request
            pass

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
