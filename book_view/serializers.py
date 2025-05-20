from rest_framework import serializers
from bookAPI.models import RecentRead, Book

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'title', 'author_name', 'published_date', 'rating']
        ref_name = 'BookView_Book'

class RecentReadSerializer(serializers.ModelSerializer):
    book = BookSerializer()

    class Meta:
        model = RecentRead
        fields = ['book', 'last_read']