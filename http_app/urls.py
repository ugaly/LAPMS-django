from django.urls import path
from . import views


urlpatterns = [
    path('add_customer', views.add_customer)    
]
