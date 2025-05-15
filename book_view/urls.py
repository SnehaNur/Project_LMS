from django.urls import path
from .views import (
    UserRecentReadBooksView,
    ToggleFavouriteBookView,
    FavouriteBooksListView,
    AdminRecentReadBooksList,
    AdminRecentReadBooksDetail
)

urlpatterns = [
    path('books/recent-reads/view/', UserRecentReadBooksView.as_view(), name='recent-reads'),
    path('admin/recent-reads/', AdminRecentReadBooksList.as_view(), name='admin-recent-reads'),
    path('admin/recent-reads/<int:pk>/', AdminRecentReadBooksDetail.as_view(), name='admin-recent-reads-detail'),
    path('favourites/<int:book_id>/', ToggleFavouriteBookView.as_view(), name='toggle-favourite'),
    path('favourites/', FavouriteBooksListView.as_view(), name='favourite-books'),
]
