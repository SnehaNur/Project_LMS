from django.db import models
from django.contrib.auth import get_user_model
from django.conf import settings 

User = get_user_model()

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    total_pages = models.PositiveIntegerField()
    rating = models.FloatField(null=True, blank=True)
    published_date = models.DateField()
    author_name = models.CharField(max_length=100)
    categories = models.ManyToManyField(Category, related_name='books')
    is_recommended = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    pdf_file = models.FileField(upload_to='books/pdfs/', blank=True, null=True)
    cover_image = models.ImageField(
    upload_to='books/covers/',  # Different directory than PDFs
    blank=True,
    null=True
    )
    summary = models.TextField(blank=True)

    def __str__(self):
        return f"{self.title} by {self.author_name}"

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Book"
        verbose_name_plural = "Books"
        
class RecentRead(models.Model):
    session_key = models.CharField(max_length=40, db_index=True)  # For anonymous users
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # Changed from 'auth.User'
        on_delete=models.CASCADE, 
        null=True, 
        blank=True
    )  # For logged-in users
    book = models.ForeignKey('Book', on_delete=models.CASCADE)
    last_read = models.DateTimeField(auto_now=True)