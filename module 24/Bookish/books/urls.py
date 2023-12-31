from django.urls import path
from .views import BookDetailsView, BookReviewView

urlpatterns = [
    path("book/<int:id>", BookDetailsView.as_view(), name="book_details"),
    path("review/<int:id>", BookReviewView.as_view(), name="review_book"),
]
