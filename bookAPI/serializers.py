from rest_framework import serializers
from .models import Book, Category
from rest_framework import serializers
from .models import RecentRead, Book

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']
        
class BookSerializer(serializers.ModelSerializer):
    pdf_url = serializers.SerializerMethodField()
    categories = CategorySerializer(many=True, read_only=True)
    category_ids = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Category.objects.all(),
        source='categories',
        write_only=True,
        required=False
    )
    review_count = serializers.IntegerField(read_only=True)
    avg_rating = serializers.FloatField(read_only=True)
    
    class Meta:
        model = Book
        fields = [
            'id', 'title', 'description', 'total_pages', 'pdf_file', 'pdf_url',
            'rating', 'published_date', 'author_name',
            'categories', 'category_ids', 'is_recommended',
            'created_at', 'updated_at', 'review_count', 'avg_rating'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'pdf_url']
        extra_kwargs = {
            'pdf_file': {'write_only': True, 'required': False}
        }

    def get_pdf_url(self, obj):
        if obj.pdf_file:
            return self.context['request'].build_absolute_uri(obj.pdf_file.url)
        return None
    
class ReadBookSerializer(serializers.ModelSerializer):
    book = serializers.StringRelatedField()

    class Meta:
        model = RecentRead
        fields = ['book', 'last_read']

