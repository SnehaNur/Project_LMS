from rest_framework import generics
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from bookAPI.models import RecentRead
from .serializers import RecentReadSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions,generics
from .models import FavouriteBook
from bookAPI.models import Book
from rest_framework.generics import ListAPIView
from bookAPI.serializers import BookSerializer  # Use existing Book serializer

class UserRecentReadBooksView(generics.ListAPIView):
    serializer_class = RecentReadSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return RecentRead.objects.filter(user=self.request.user).order_by('-last_read')
    

class AdminRecentReadBooksList(generics.ListAPIView):
    serializer_class = RecentReadSerializer
    permission_classes = [permissions.IsAdminUser]
    queryset = RecentRead.objects.all().order_by('-last_read')
    filter_backends = [] 

class AdminRecentReadBooksDetail(generics.RetrieveDestroyAPIView):
    serializer_class = RecentReadSerializer
    permission_classes = [permissions.IsAdminUser]
    queryset = RecentRead.objects.all()
    lookup_field = 'pk'

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {"detail": "Recent read entry deleted successfully."},
            status=status.HTTP_200_OK
        )
    
class ToggleFavouriteBookView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, book_id):
        user = request.user
        try:
            book = Book.objects.get(id=book_id)
        except Book.DoesNotExist:
            return Response({'error': 'Book not found'}, status=status.HTTP_404_NOT_FOUND)

        fav, created = FavouriteBook.objects.get_or_create(user=user, book=book)
        if not created:
            fav.delete()
            return Response({'message': 'Book removed from favourites'}, status=status.HTTP_200_OK)
        return Response({'message': 'Book added to favourites'}, status=status.HTTP_201_CREATED)


class FavouriteBooksListView(ListAPIView):
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Book.objects.filter(favouritebook__user=self.request.user)
