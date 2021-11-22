from django.contrib.auth.models import AbstractUser
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_delete


class Client(AbstractUser):
    first_name = models.CharField(max_length=255, null=True)
    name = models.CharField(max_length=255, null=True)
    remaining_balance = models.FloatField(default=50.0)
    email = models.EmailField(max_length=255, null=True)
    # Required fields
    REQUIRED_FIELDS = ['first_name', 'name', 'email']