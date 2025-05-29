from django.urls import path
from .views import (
    BookDetailView, 
    BookReviewCreateView,
    BookReviewListView,
    AdminReviewListView,
    AdminReviewDetailView,
    BookSummaryView
)

urlpatterns = [
    path('user/books/<int:pk>/', BookDetailView.as_view(), name='book-detail'),
    path('user/books/<int:book_id>/reviews/create/', BookReviewCreateView.as_view(), name='review-create'),
    path('user/books/<int:book_id>/reviews/', BookReviewListView.as_view(), name='review-list'),
    path('user/books/<int:pk>/summary/', BookSummaryView.as_view(), name='book-summary'),
    
    # Admin URLs
    path('admin/reviews/', AdminReviewListView.as_view(), name='admin-review-list'),
    path('admin/reviews/<int:pk>/', AdminReviewDetailView.as_view(), name='admin-review-detail'),
]