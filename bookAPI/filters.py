from django_filters import rest_framework as filters
from .models import Book, Category

class BookFilter(filters.FilterSet):
    category_name = filters.CharFilter(field_name='categories__name', lookup_expr='iexact')
    is_recommended = filters.BooleanFilter()
    
    class Meta:
        model = Book
        fields = {
            'author_name': ['exact'],
        }