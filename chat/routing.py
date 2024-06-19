from django.urls import path
from chat.consumers import ChatConsumer
from .consumers import CustomerConsumer
from .consumers import ComplaintConsumer
from .consumers import QuestionConsumer

from . import views


# urlpatterns = [
#     path(r'ws/chat/$', ChatConsumer.as_asgi()),
#     path(r'ws/customers/$', CustomerConsumer.as_asgi()),
# ]



urlpatterns = [
    path('ws/chat/', ChatConsumer.as_asgi()),
    path('ws/customers/', CustomerConsumer.as_asgi()),

    path('add_customer', views.add_customer),



    path('ws/complaints/', ComplaintConsumer.as_asgi()),
    path('ws/questions/', QuestionConsumer.as_asgi()),
]
