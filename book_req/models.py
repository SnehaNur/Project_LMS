from django.db import models
from django.conf import settings

class BookRequest(models.Model):
    PENDING = 'PENDING'
    APPROVED = 'APPROVED'
    REJECTED = 'REJECTED'
    
    STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (APPROVED, 'Approved'),
        (REJECTED, 'Rejected'),
    ]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    book = models.ForeignKey('bookAPI.Book', on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=PENDING)
    request_date = models.DateTimeField(auto_now_add=True)
    processed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='processed_requests'
    )
    processed_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-request_date']
        verbose_name = 'Book Request'
        verbose_name_plural = 'Book Requests'

    def __str__(self):
        return f"{self.user.email} - {self.book.title} ({self.status})"
