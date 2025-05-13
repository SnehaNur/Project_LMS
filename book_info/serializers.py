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
    class Meta:
        model = Review
        fields = ['id', 'user', 'text', 'rating', 'created_at']


