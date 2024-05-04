import json
import traceback

from django.db.models import Avg
from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.exceptions import NotFound
from rest_framework.request import Request

from vendor.models import Vendor, HistoricalPerformance
from vendor.serializers import VendorSerializer, VendorPerformance


# Create your views here.


@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def vendors(request, vendor_id=None):
    response = {"status_code": 500, "message": "Internal Server Error"}
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
            # Handle DELETE request
            pass

        # response['status_code'] = 200
        # response['message'] = "Success"
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
