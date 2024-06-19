# # views.py
# from rest_framework import status
# from rest_framework.decorators import api_view
# from rest_framework.response import Response
# from .models import Customer
# from .serializers import CustomerSerializer

# @api_view(['POST'])
# def create_customer(request):
#     serializer = CustomerSerializer(data=request.data)
#     if serializer.is_valid():
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# @api_view(['GET'])
# def list_customers(request):
#     customers = Customer.objects.all()
#     serializer = CustomerSerializer(customers, many=True)
#     return Response(serializer.data)




# myapp/views.py

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .models import Customer
from .consumers import CustomerConsumer
import json

@csrf_exempt
@transaction.atomic
def add_customer(request):
    print('bbbbbbbbbbbbb',request)
    if request.method == 'POST':
        # Extract data from the request
        data = json.loads(request.body)
        full_name = data.get('full_name')
        phone_number = data.get('phone_number')
        location = data.get('location')
        print(request)



        try:
            # Create a new customer object
            customer = Customer.objects.create(
                full_name=full_name,
                phone_number=phone_number,
                location=location,
                # created_by=request.user  # Assuming the user is authenticated
            )

            # Broadcast the new customer data to WebSocket consumers
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                'customer_group',
                {
                    'type': 'new_customer',
                    'customer': {
                        'id': customer.id,
                        'full_name': customer.full_name,
                        'phone_number': customer.phone_number,
                        'location': customer.location
                    }
                }
            )

            return JsonResponse({'message': 'Customer added successfully', 'customer': customer.id})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    else:
        return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)
