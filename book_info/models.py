from django.db import models
from bookAPI.models import Book
from django.conf import settings

class Review(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.TextField()
    rating = models.PositiveIntegerField(choices=[(i, i) for i in range(1, 6)])  # 1-5 stars
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('book', 'user')  # Prevent duplicate reviews
        ordering = ['-created_at']  # Newest first