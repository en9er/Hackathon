from django.db import models
from client.models import Client
from django.urls import reverse


class ReceiptCategory(models.Model):
    name = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return self.name


def get_request_url(obj, viewname):
    model = obj.__class__.meta.model_name
    return reverse(viewname, kwargs={'model':model, 'slug':obj.__str__()})


class Receipt(models.Model):
    photo = models.CharField(max_length=256)
    sum = models.FloatField(default=0)
    date = models.DateField()
    category = models.CharField(max_length=255, null=True)
    owner = models.ForeignKey(to=Client, on_delete=models.CASCADE, null=True)
    proceed = models.BooleanField(default=False)

    def __str__(self):
        return self.date.__str__()