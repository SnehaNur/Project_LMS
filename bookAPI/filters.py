from django_filters import rest_framework as filters
from .models import Book, Category

class BookFilter(filters.FilterSet):
    category_id = filters.NumberFilter(field_name='categories__id')
    category_name = filters.CharFilter(field_name='categories__name', lookup_expr='iexact')
    is_recommended = filters.BooleanFilter()
    min_rating = filters.NumberFilter(field_name='rating', lookup_expr='gte')
    max_rating = filters.NumberFilter(field_name='rating', lookup_expr='lte')
    
    class Meta:
        model = Book
        fields = {
            'author_name': ['exact', 'icontains'],
            'published_date': ['exact', 'year', 'year__gt', 'year__lt'],
        }