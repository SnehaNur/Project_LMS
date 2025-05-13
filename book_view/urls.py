from django.urls import path
from .views import UserRecentReadBooksView,ToggleFavouriteBookView,FavouriteBooksListView

urlpatterns = [
    path('books/recent-reads/view/', UserRecentReadBooksView.as_view(), name='recent-reads'),
    path('favourites/<int:book_id>/', ToggleFavouriteBookView.as_view(), name='toggle-favourite'),
    path('favourites/', FavouriteBooksListView.as_view(), name='favourite-books'),
]
