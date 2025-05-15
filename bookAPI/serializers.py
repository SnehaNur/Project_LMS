from rest_framework import serializers
from .models import Book, Category, RecentRead

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']
        
class BookSerializer(serializers.ModelSerializer):
    # Method fields (not in model)
    pdf_url = serializers.SerializerMethodField()
    cover_image_url = serializers.SerializerMethodField()
    
    # Related fields
    categories = CategorySerializer(many=True, read_only=True)
    category_ids = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Category.objects.all(),
        source='categories',
        write_only=True,
        required=False
    )
    
    # Computed fields
    review_count = serializers.IntegerField(read_only=True)
    avg_rating = serializers.FloatField(read_only=True)
    
    class Meta:
        model = Book
        fields = [
            # Core fields
            'id', 'title', 'description', 'total_pages', 
            'rating', 'published_date', 'author_name',
            'is_recommended', 'created_at', 'updated_at', 'summary',
            
            # File fields
            'pdf_file', 'pdf_url', 'cover_image', 'cover_image_url',
            
            # Relation fields
            'categories', 'category_ids',
            
            # Computed fields
            'review_count', 'avg_rating'
        ]
        read_only_fields = [
            'id', 'created_at', 'updated_at', 
            'pdf_url', 'cover_image_url',
            'review_count', 'avg_rating'
        ]
        extra_kwargs = {
            'pdf_file': {'write_only': True, 'required': False},
            'cover_image': {'write_only': True, 'required': False}
        }

    def get_pdf_url(self, obj):
        """Generate absolute URL for PDF file"""
        if obj.pdf_file:
            return self.context['request'].build_absolute_uri(obj.pdf_file.url)
        return None

    def get_cover_image_url(self, obj):
        """Generate absolute URL for cover image"""
        if obj.cover_image:
            return self.context['request'].build_absolute_uri(obj.cover_image.url)
        return None
    
class ReadBookSerializer(serializers.ModelSerializer):
    book = serializers.StringRelatedField()

    class Meta:
        model = RecentRead
        fields = ['book', 'last_read']