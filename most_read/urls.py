from django.urls import path
from .views import MostReadBooksView,BookDetailAdminView,BookReadersView

urlpatterns = [
    path('most-read/view/', MostReadBooksView.as_view(), name='most-read-books'),
    path('most-read-books/<int:id>/', BookDetailAdminView.as_view(), name='admin-book-detail'),
    path('book-readers/', BookReadersView.as_view(), name='book-readers'),
]