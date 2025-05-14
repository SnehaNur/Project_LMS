from rest_framework import serializers
from .models import BorrowRequest
from django.utils import timezone
from datetime import timedelta

class BorrowRequestSerializer(serializers.ModelSerializer):
    book_title = serializers.CharField(source='book.title', read_only=True)
    user_email = serializers.CharField(source='user.email', read_only=True)
    can_process = serializers.SerializerMethodField()

    class Meta:
        model = BorrowRequest
        fields = [
            'id', 'book', 'book_title', 'user', 'user_email', 
            'status', 'request_date', 'approved_date', 'return_date',
            'due_date', 'processed_by', 'can_process'
        ]
        read_only_fields = [
            'user', 'status', 'request_date', 'approved_date',
            'return_date', 'due_date', 'processed_by'
        ]

    def get_can_process(self, obj):
        request = self.context.get('request')
        return request and (request.user.is_staff or request.user.is_superuser)

    def validate(self, data):
        user = self.context['request'].user
        book = data['book']
        
        # Check if user already has a pending request for this book
        if BorrowRequest.objects.filter(
            user=user, 
            book=book, 
            status__in=[BorrowRequest.PENDING, BorrowRequest.APPROVED]
        ).exists():
            raise serializers.ValidationError(
                "You already have an active or pending request for this book."
            )
            
        return data