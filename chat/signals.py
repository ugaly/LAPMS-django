from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Customer  # Import your model here
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import json

# @receiver(post_save, sender=Customer)
# def send_customer_update(sender, instance, created, **kwargs):
#     if created:
#         # Broadcast new customer data to WebSocket clients
#         channel_layer = get_channel_layer()
#         async_to_sync(channel_layer.group_send)(
#             "customer_group",
#             {
#                 'type': 'new_customer',
#                 'customer': {
#                     'id': instance.id,
#                     'full_name': instance.full_name,
#                     'phone_number': instance.phone_number,
#                     'location': instance.location,
#                 }
#             }
#         )



@receiver(post_save, sender=Customer)
def send_customer_update(sender, instance, created, **kwargs):
    if created and not getattr(instance, '_signal_sent', False):
        # Set the flag to True to indicate that the signal has been sent
        instance._signal_sent = True

        # Broadcast new customer data to WebSocket clients
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            "customer_group",
            {
                'type': 'new_customer',
                'customer': {
                    'id': instance.id,
                    'full_name': instance.full_name,
                    'phone_number': instance.phone_number,
                    'location': instance.location,
                }
            }
        )