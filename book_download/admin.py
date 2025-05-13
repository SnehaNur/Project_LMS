from django.contrib import admin
from .models import DownloadedBook

@admin.register(DownloadedBook)
class DownloadedBookAdmin(admin.ModelAdmin):
    list_display = ('user', 'book', 'downloaded_at', 'download_count')
    list_filter = ('downloaded_at',)
    search_fields = ('user__username', 'book__title')
