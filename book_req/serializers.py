from rest_framework import serializers
from .models import BookRequest

class BookRequestSerializer(serializers.ModelSerializer):
    book_title = serializers.CharField(source='book.title', read_only=True)
    user_email = serializers.CharField(source='user.email', read_only=True)
    processed_by_email = serializers.CharField(source='processed_by.email', read_only=True)
    can_approve = serializers.SerializerMethodField()

    class Meta:
        model = BookRequest
        fields = [
            'id', 'book', 'book_title', 'user', 'user_email', 
            'status', 'request_date', 'processed_by', 'processed_by_email',
            'processed_date', 'can_approve'
        ]
        read_only_fields = [
            'user', 'status', 'request_date', 
            'processed_by', 'processed_date', 'processed_by_email',
            'book_title', 'user_email', 'can_approve'
        ]

    def get_can_approve(self, obj):
        request = self.context.get('request')
        return request and request.user.is_superuser

    def validate(self, data):
        user = self.context['request'].user
        book = data.get('book')
        
        if not book:
            return data
            
        # Prevent duplicate pending requests
        if BookRequest.objects.filter(
            user=user, 
            book=book, 
            status=BookRequest.PENDING
        ).exists():
            raise serializers.ValidationError(
                "You already have a pending request for this book."
            )
        return data