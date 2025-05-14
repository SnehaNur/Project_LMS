from rest_framework import generics, permissions,status
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from .serializers import UserDetailSerializer,UserInfoSerializer
from bookAPI.models import Book


User = get_user_model()

class AllUsersListView(generics.ListAPIView):
    serializer_class = UserDetailSerializer
    permission_classes = [permissions.IsAdminUser]
    queryset = User.objects.filter(is_staff=False).count()
    
    def get_queryset(self):
        # Return all users ordered by ID (you can change the ordering)
        return User.objects.filter(is_staff=False).order_by('id')
    
class TotalUsersView(generics.GenericAPIView):
    permission_classes = [permissions.IsAdminUser]
    
    def get(self, request):
        # Count only non-admin users
        total_users = User.objects.filter(is_staff=False).count()
        return Response({'total_users': total_users})
    
class TotalBooksView(generics.GenericAPIView):
    permission_classes = [permissions.IsAdminUser]
    
    def get(self, request):
        total_books = Book.objects.count()
        return Response({
            'total_books': total_books,
        })

class UserInfoView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserInfoSerializer
    permission_classes = [permissions.IsAdminUser]  # Only admin can access
    queryset = User.objects.filter(is_staff=False)
    lookup_field = 'id'

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {"detail": "User deleted!"},
            status=status.HTTP_200_OK
        )

    def perform_destroy(self, instance):
        # Permanent deletion
        instance.delete()