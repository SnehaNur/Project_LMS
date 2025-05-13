from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import BookRequest
from .serializers import BookRequestSerializer
from rest_framework import viewsets, permissions,status
from django.utils import timezone

class BookRequestViewSet(viewsets.ModelViewSet):
    serializer_class = BookRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_superuser:
            return BookRequest.objects.all()
        return BookRequest.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAdminUser])
    def approve(self, request, pk=None):
        book_request = self.get_object()
        book_request.status = BookRequest.APPROVED
        book_request.processed_by = request.user
        book_request.processed_date = timezone.now()
        book_request.save()
        return Response({'status': 'approved'}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAdminUser])
    def reject(self, request, pk=None):
        book_request = self.get_object()
        book_request.status = BookRequest.REJECTED
        book_request.processed_by = request.user
        book_request.processed_date = timezone.now()
        book_request.save()
        return Response({'status': 'rejected'}, status=status.HTTP_200_OK)
