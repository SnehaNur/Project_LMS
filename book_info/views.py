from rest_framework import generics, permissions
from bookAPI.models import Book
from .models import Review
from .serializers import BookDetailSerializer, ReviewSerializer

class BookDetailView(generics.RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookDetailSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

# book_info/views.py
class BookReviewListView(generics.ListAPIView):  # GET
    serializer_class = ReviewSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        book_id = self.kwargs['book_id']
        return Review.objects.filter(book_id=book_id)

class BookReviewCreateView(generics.CreateAPIView):  # POST
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        book_id = self.kwargs['book_id']
        serializer.save(user=self.request.user, book_id=book_id)

'''

class ReviewCreateView(generics.CreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        # Get book_id from URL kwargs and set it automatically
        serializer.save(
            user=self.request.user,
            book_id=self.kwargs['pk']  # This comes from the URL pattern
        )

class BookReviewListView(generics.ListAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]  # Or IsAuthenticated
    
    def get_queryset(self):
        book_id = self.kwargs['book_id']
        return Review.objects.filter(book_id=book_id)

    def perform_create(self, serializer):
        book_id = self.kwargs['book_id']
        serializer.save(user=self.request.user, book_id=book_id)

'''