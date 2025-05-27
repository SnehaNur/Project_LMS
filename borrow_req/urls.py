from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BorrowRequestViewSet,BookAvailabilityViewSet

router = DefaultRouter()
router.register(r'borrow-requests', BorrowRequestViewSet, basename='borrowrequest')
router.register(r'admin/book-availability', BookAvailabilityViewSet, basename='bookavailability')

urlpatterns = [
    path('', include(router.urls)),
]