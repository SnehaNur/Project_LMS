from rest_framework import generics, permissions, status
from rest_framework.response import Response
from bookAPI.models import Book
from .models import Review
from .serializers import BookDetailSerializer, ReviewSerializer, AdminReviewSerializer,BookSummarySerializer
from django.contrib.auth.models import User

class BookDetailView(generics.RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookDetailSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class BookReviewListView(generics.ListAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        book_id = self.kwargs['book_id']
        return Review.objects.filter(book_id=book_id, is_visible=True)  # Only show visible reviews

class BookReviewCreateView(generics.CreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        book_id = self.kwargs['book_id']
        serializer.save(user=self.request.user, book_id=book_id)

class AdminReviewListView(generics.ListAPIView):
    serializer_class = AdminReviewSerializer
    permission_classes = [permissions.IsAdminUser]
    queryset = Review.objects.all()

class AdminReviewDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = AdminReviewSerializer
    permission_classes = [permissions.IsAdminUser]
    queryset = Review.objects.all()

    def perform_destroy(self, instance):
        # Soft delete by making it invisible instead of actual deletion
        instance.is_visible = False
        instance.save()

    def update(self, request, *args, **kwargs):
        # Allow admin to modify visibility or content
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)
    
class BookSummaryView(generics.RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSummarySerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = 'pk'