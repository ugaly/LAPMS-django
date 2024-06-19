from django.db import models
from django_currentuser.db.models import CurrentUserField

# Create your models here.
class Customer(models.Model):
    full_name = models.CharField(max_length=100, null=True, blank=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    location = models.CharField(max_length=100, null=True, blank=True)
    created_by = CurrentUserField(related_name='asset_creator', null=True, blank=True)

