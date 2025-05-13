from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from .models import Book, Category, RecentRead
from .serializers import BookSerializer, CategorySerializer,ReadBookSerializer
from django_filters.rest_framework import DjangoFilterBackend
from .filters import BookFilter
from rest_framework import generics, permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework import status
from django.db.models import Count, F


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'id'
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']


class BookViewSet(viewsets.ModelViewSet):
    serializer_class = BookSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = BookFilter
    search_fields = ['title', 'description', 'author_name', 'categories__name']

    ordering_fields = [
        'title', 
        'published_date', 
        'rating', 
        'created_at',
        'popular',
        'new_release'
    ]

    def get_queryset(self):
        queryset = Book.objects.all().prefetch_related('categories')

        # Add custom annotations for ordering
        ordering = self.request.GET.get('ordering', '')
        if 'popular' in ordering:
            queryset = queryset.annotate(popular=Count('recentread'))
        if 'new_release' in ordering:
            queryset = queryset.annotate(new_release=F('published_date'))

        # Filter by recent reads (authenticated or anonymous)
        recent_reads = self.request.GET.get('recent_reads', '').lower()
        if recent_reads in ['true', '1', 'yes']:
            if self.request.user.is_authenticated:
                recent_book_ids = RecentRead.objects.filter(
                    user=self.request.user
                ).values_list('book_id', flat=True)
            else:
                session_key = self.request.session.session_key
                if session_key:
                    recent_book_ids = RecentRead.objects.filter(
                        session_key=session_key
                    ).values_list('book_id', flat=True)
                else:
                    recent_book_ids = []

            queryset = queryset.filter(id__in=recent_book_ids)

        return queryset

    def perform_create(self, serializer):
        pdf_file = self.request.FILES.get('pdf_file')
        serializer.save(pdf_file=pdf_file)

    def perform_update(self, serializer):
        pdf_file = self.request.FILES.get('pdf_file')
        if pdf_file is not None:
            serializer.save(pdf_file=pdf_file)
        else:
            serializer.save()

    @action(detail=True, methods=['post'])
    def mark_as_read(self, request, pk=None):
        """Endpoint to mark a book as recently read"""
        book = self.get_object()

        if request.user.is_authenticated:
            RecentRead.objects.update_or_create(
                user=request.user,
                book=book,
                defaults={'last_read': timezone.now()}
            )
        else:
            session_key = request.session.session_key
            if not session_key:
                request.session.create()
                session_key = request.session.session_key

            RecentRead.objects.update_or_create(
                session_key=session_key,
                book=book,
                defaults={'last_read': timezone.now()}
            )

        return Response({'status': 'book marked as read'})

class BookSearchView(generics.ListAPIView):
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        queryset = Book.objects.all()

        title = self.request.query_params.get('title')
        author = self.request.query_params.get('author')
        category = self.request.query_params.get('category')
        published_year = self.request.query_params.get('published_year')
        rating = self.request.query_params.get('rating')

        if title:
            queryset = queryset.filter(title__icontains=title)
        if author:
            queryset = queryset.filter(author_name__icontains=author)
        if category:
            queryset = queryset.filter(categories__name__icontains=category)
        if published_year:
            queryset = queryset.filter(published_date__year=published_year)
        if rating:
            queryset = queryset.filter(rating__gte=rating)

        return queryset.distinct()


class ReadBooksView(generics.ListAPIView):
    serializer_class = ReadBookSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return RecentRead.objects.filter(user=self.request.user).select_related('book').order_by('-last_read')

class MarkAsReadView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            book = Book.objects.get(pk=pk)
        except Book.DoesNotExist:
            return Response({"detail": "Book not found"}, status=status.HTTP_404_NOT_FOUND)

        recent, created = RecentRead.objects.get_or_create(
            user=request.user,
            book=book,
            defaults={"session_key": request.session.session_key or ""}
        )
        if not created:
            recent.save()  # This will update `last_read` because of auto_now

        return Response({"detail": "Book marked as read"}, status=status.HTTP_200_OK)
