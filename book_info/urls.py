from django.urls import path
from .views import BookDetailView, BookReviewCreateView,BookReviewListView

urlpatterns = [
    path('books/<int:pk>/', BookDetailView.as_view(), name='book-detail'),
    path('books/<int:book_id>/reviews/create/', BookReviewCreateView.as_view(), name='review-create'),
    path('books/<int:book_id>/reviews/', BookReviewListView.as_view(), name='review-list'),
]