from typing import Any
from django.views.generic import DetailView, CreateView
from .models import BookModel, ReviewModel
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import ReviewForm
from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import redirect
from .models import ReviewModel

# Create your views here.


class BookDetailsView(DetailView):
    template_name = "books/book_details.html"
    model = BookModel
    pk_url_kwarg = "id"
    context_object_name = "book"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        id = self.kwargs['id']
        book = BookModel.objects.get(pk=id)
        reviews = ReviewModel.objects.filter(book=book)
        context.update({
            'reviews': reviews
        })
        return context

# def returnBook(request, id) :
#     transaction = TransactionModel.objects.get(pk=id)


class BookReviewView(LoginRequiredMixin, CreateView):
    template_name = "books/book_review.html"
    model = ReviewModel
    form_class = ReviewForm
    success_url = reverse_lazy("profile")

    def get_initial(self):
        id = self.kwargs['id']
        book = BookModel.objects.get(pk=id)
        initial = {'book': book, 'user': self.request.user}
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        id = self.kwargs['id']
        book = BookModel.objects.get(pk=id)
        context.update({
            'book': book
        })
        return context

    def form_valid(self, form):
        id = self.kwargs['id']
        book = BookModel.objects.get(pk=id)
        isAlreadyReviewed = ReviewModel.objects.filter(
            book=book, user=self.request.user).count()
        if isAlreadyReviewed >= 1:
            messages.info(self.request, "You have already reviewed this book.")
            return redirect("profile")
        else:
            messages.success(self.request, "Thanks for your valuable Reviews")
        return super().form_valid(form)
