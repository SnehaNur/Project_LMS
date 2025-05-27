from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import BorrowRequest,BookAvailability
from .serializers import BorrowRequestSerializer,BookAvailabilitySerializer
from rest_framework import permissions
from django.utils import timezone
from datetime import timedelta
from rest_framework.permissions import IsAdminUser


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
         return Response({'error': 'Request is not in pending state'}, status=400)

        # check available copies
        availability = BookAvailability.objects.get(book=borrow_request.book)
        if availability.available_copies <= 0:
         return Response({'error': 'No available copies for this book'}, status=400)

        borrow_request.status = BorrowRequest.APPROVED
        borrow_request.processed_by = request.user
        borrow_request.approved_date = timezone.now()
        borrow_request.due_date = timezone.now() + timedelta(days=14)
        borrow_request.save()

        # decrease available copies
        availability.available_copies -= 1
        availability.save()

        return Response({'status': 'approved', 'due_date': borrow_request.due_date})

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
         return Response({'error': 'Only approved books can be marked as returned'}, status=400)

        borrow_request.status = BorrowRequest.RETURNED
        borrow_request.return_date = timezone.now()
        borrow_request.save()

        # increase available copies
        availability = BookAvailability.objects.get(book=borrow_request.book)
        availability.available_copies += 1
        availability.save()

        return Response({'status': 'returned'})

    
class BookAvailabilityViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = BookAvailability.objects.select_related('book').all()
    serializer_class = BookAvailabilitySerializer
    permission_classes = [IsAdminUser]

    @action(detail=True, methods=['post'], permission_classes=[IsAdminUser])
    def add_copies(self, request, pk=None):
        try:
            book_availability = self.get_object()
            count = int(request.data.get('count', 0))
            if count < 1:
                return Response({'error': 'Count must be at least 1'}, status=400)
            book_availability.total_copies += count
            book_availability.available_copies += count
            book_availability.save()
            return Response({
                'message': f"{count} copies added.",
                'total_copies': book_availability.total_copies,
                'available_copies': book_availability.available_copies
            })
        except Exception as e:
            return Response({'error': str(e)}, status=500)