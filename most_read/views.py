from rest_framework.views import APIView
from rest_framework.response import Response
from bookAPI.models import Book,RecentRead
from django.db.models import Count
from bookAPI.serializers import BookSerializer  # or create a new one with reader_count
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAdminUser
from rest_framework.generics import ListAPIView
from .serializers import ReaderBookSerializer

class MostReadBooksView(APIView):
    def get(self, request):
        books = Book.objects.annotate(
            reader_count=Count('recentread__user', distinct=True)
        ).order_by('-reader_count')

        data = [
            {
                "book_id": book.id,
                "title": book.title,
                "reader_count": book.reader_count
            }
            for book in books
        ]
        return Response(data)
    

class BookDetailAdminView(RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAdminUser]
    lookup_field = 'id'

class BookReadersView(ListAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = ReaderBookSerializer

    def get_queryset(self):
        return RecentRead.objects.select_related('user', 'book') \
            .exclude(user__isnull=True) \
            .order_by('-last_read')  # Most recent first
