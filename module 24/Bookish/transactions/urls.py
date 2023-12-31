from django.urls import path
from .views import DepositView, BorrowView, ReturnBookView

urlpatterns = [
    path("deposit/", DepositView.as_view(), name="deposit"),
    path("borrow/<int:id>", BorrowView.as_view(), name="borrow"),
    path("return/<int:id>", ReturnBookView.as_view(), name="return")
]
