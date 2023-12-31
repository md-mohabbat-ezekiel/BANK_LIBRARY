from django.db import models
from customers.models import CustomerModel
from books.models import BookModel
from .constants import TRANSACTION_TYPES
# Create your models here.


class TransactionModel(models.Model):
    customer = models.ForeignKey(
        CustomerModel, related_name="transaction", on_delete=models.CASCADE)
    transaction_type = models.IntegerField(
        choices=TRANSACTION_TYPES)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    balance_after_transaction = models.DecimalField(
        max_digits=12, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)
    book = models.ForeignKey(
        BookModel, related_name="borrows", on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self) -> str:
        return str(self.customer.customer_id)
