from rest_framework import serializers
from bookAPI.models import Book
from .models import Review
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']  # Customize as needed

class BookDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'

class ReviewSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)  # Show user details
    
    class Meta:
        model = Review
        fields = ['id', 'user', 'text', 'rating', 'created_at', 'is_visible']
        read_only_fields = ['id', 'user', 'created_at']  # These fields can't be modified directly

class AdminReviewSerializer(ReviewSerializer):
    class Meta(ReviewSerializer.Meta):
        fields = ReviewSerializer.Meta.fields + ['book']  # Include book field for admin

# Add this to your existing serializers.py
class BookSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'title', 'summary']  # img needed here