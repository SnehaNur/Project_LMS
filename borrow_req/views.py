from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import BorrowRequest
from .serializers import BorrowRequestSerializer
from rest_framework import permissions
from django.utils import timezone
from datetime import timedelta

class BorrowRequestViewSet(viewsets.ModelViewSet):
    serializer_class = BorrowRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_staff or self.request.user.is_superuser:
            return BorrowRequest.objects.all()
        return BorrowRequest.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAdminUser])
    def approve(self, request, pk=None):
        borrow_request = self.get_object()
        if borrow_request.status != BorrowRequest.PENDING:
            return Response(
                {'error': 'Request is not in pending state'},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        borrow_request.status = BorrowRequest.APPROVED
        borrow_request.processed_by = request.user
        borrow_request.approved_date = timezone.now()
        borrow_request.due_date = timezone.now() + timedelta(days=14)  # 2 weeks loan period
        borrow_request.save()
        
        return Response({'status': 'approved', 'due_date': borrow_request.due_date}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAdminUser])
    def reject(self, request, pk=None):
        borrow_request = self.get_object()
        if borrow_request.status != BorrowRequest.PENDING:
            return Response(
                {'error': 'Request is not in pending state'},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        borrow_request.status = BorrowRequest.REJECTED
        borrow_request.processed_by = request.user
        borrow_request.save()
        
        return Response({'status': 'rejected'}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAdminUser])
    def mark_returned(self, request, pk=None):
        borrow_request = self.get_object()
        if borrow_request.status != BorrowRequest.APPROVED:
            return Response(
                {'error': 'Only approved books can be marked as returned'},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        borrow_request.status = BorrowRequest.RETURNED
        borrow_request.return_date = timezone.now()
        borrow_request.save()
        
        return Response({'status': 'returned'}, status=status.HTTP_200_OK)