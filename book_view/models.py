from django.db import models
from django.conf import settings
from bookAPI.models import Book  # Import Book from the bookAPI app

class FavouriteBook(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    marked_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'book')  # Prevent duplicate favourites

    def __str__(self):
        return f"{self.user.email} -> {self.book.title}"
