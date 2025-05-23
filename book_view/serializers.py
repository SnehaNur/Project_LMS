from rest_framework import serializers
from bookAPI.models import RecentRead, Book

class BookSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'title']

class RecentReadSerializer(serializers.ModelSerializer):
    book = BookSimpleSerializer()

    class Meta:
        model = RecentRead
        fields = ['book', 'last_read']