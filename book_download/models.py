from django.db import models
from django.conf import settings
from bookAPI.models import Book

class DownloadedBook(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='downloaded_books'
    )
    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        related_name='downloads'
    )
    downloaded_at = models.DateTimeField(auto_now_add=True)
    download_count = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ('user', 'book')
        ordering = ['-downloaded_at']

    def __str__(self):
        return f"{self.user.username} downloaded {self.book.title} (x{self.download_count})"
