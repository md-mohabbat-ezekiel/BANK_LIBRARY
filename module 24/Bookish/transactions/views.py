from django.http import HttpResponse
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, View
from .models import TransactionModel
from .forms import DepositForm, BorrowForm
from .constants import DEPOSIT, RETURN, BORROW
from django.contrib import messages
from django.urls import reverse_lazy
from books.models import BookModel
from email_system.utils.email import send_transaction_emails
# Create your views here.


class TransactionViewMixin(LoginRequiredMixin, CreateView):
    template_name = "transactions/transaction_form.html"
    success_url = reverse_lazy("home")
    model = TransactionModel
    title = ""

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({
            'customer': self.request.user.customer
        })
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'title': self.title
        })
        return context


class DepositView(TransactionViewMixin):
    form_class = DepositForm
    title = "Deposit"

    def get_initial(self):
        initial = {'transaction_type': DEPOSIT}
        return initial

    def form_valid(self, form):
        amount = form.cleaned_data.get('amount')
        customer = self.request.user.customer

        customer.balance += amount

        customer.save(
            update_fields=['balance']
        )

        send_transaction_emails(
            self.request.user,
            self.request.user.email,
            f"Balance Deposited Customer ID : {customer.customer_id}",
            f"""Your deposit request for ${amount} has successfully completed. After deposit your total amount is {customer.balance}""")

        messages.success(self.request, f"""{"{:,.2f}".format(
            float(amount))}$ was deposited to your account successfully""")

        return super().form_valid(form)


class BorrowView(TransactionViewMixin):
    form_class = BorrowForm
    title = "Borrow Book"

    def get_initial(self):
        id = self.kwargs['id']
        book = BookModel.objects.get(id=id)
        initial = {'transaction_type': BORROW,
                   'book': book, 'amount': book.borrowing_price}
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        id = self.kwargs['id']
        book = BookModel.objects.get(id=id)
        context.update({
            'book': book,
            'isBookView': True
        })
        return context

    def form_valid(self, form):
        customer = self.request.user.customer
        id = self.kwargs['id']
        book = BookModel.objects.get(id=id)
        # Get the amount from the form
        amount = book.borrowing_price

        if customer.balance < amount:
            messages.error(self.request, "You don't have sufficient money")
            return redirect("profile")

        customer.balance -= amount

        customer.save(
            update_fields=['balance']
        )

        send_transaction_emails(
            self.request.user,
            self.request.user.email,
            f"Book has been borrowed by Customer : {customer.customer_id}",
            f"""You have successfully borrowed this book : ({book.title}) cost of : ${amount}""")

        messages.success(self.request, f""" Book has been borrowed and your current balance is ${
                         customer.balance} """)

        return super().form_valid(form)


class ReturnBookView(LoginRequiredMixin, View):
    def get(self, request, id):
        transaction = get_object_or_404(TransactionModel, pk=id)

        transaction.transaction_type = RETURN
        customer = self.request.user.customer
        customer.balance += transaction.amount
        customer.save()
        transaction.save()

        messages.success(
            self.request,
            f"""The book {transaction.book.title} has been returned,and your balance has been refunded by ${transaction.amount}."""
        )

        send_transaction_emails(
            self.request.user,
            self.request.user.email,
            f"""Thanks for returning the book by Customer ID : {
                customer.customer_id}""",
            f"""Your book amount ${transaction.amount} has been refunded""")

        return redirect("profile")
