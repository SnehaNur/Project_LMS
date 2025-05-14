from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BorrowRequestViewSet

router = DefaultRouter()
router.register(r'borrow-requests', BorrowRequestViewSet, basename='borrowrequest')

urlpatterns = [
    path('', include(router.urls)),
]