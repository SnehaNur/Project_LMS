from rest_framework import serializers
from bookAPI.serializers import BookSerializer
from .models import DownloadedBook

class DownloadedBookSerializer(serializers.ModelSerializer):
    book = BookSerializer(read_only=True)
    
    class Meta:
        model = DownloadedBook
        fields = ['book', 'downloaded_at', 'download_count']