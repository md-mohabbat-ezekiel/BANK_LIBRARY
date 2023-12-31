from django.db import models
from django.contrib.auth.models import User
from .constants import GENDER_TYPES

# Create your models here.


class CustomerModel(models.Model):
    user = models.OneToOneField(
        User, related_name="customer", on_delete=models.CASCADE)
    customer_id = models.IntegerField(unique=True)
    phone_no = models.CharField(max_length=100)
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    gender = models.CharField(choices=GENDER_TYPES)
    street_address = models.CharField(max_length=100)
    city = models.CharField(max_length=100)

    def __str__(self) -> str:
        return str(self.customer_id)
