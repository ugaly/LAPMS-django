# urls.py
from django.urls import path
from . import views

urlpatterns = [
    # path('customers/', views.list_customers),
    # path('customers/create/', views.create_customer),
    path('add_customer', views.add_customer)
]
