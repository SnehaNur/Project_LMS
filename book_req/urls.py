from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BookRequestViewSet,AdminBookRequestCountView

router = DefaultRouter()
router.register(r'book-requests', BookRequestViewSet, basename='bookrequest')
router.register(r'admin/book-requests', AdminBookRequestCountView, basename='admin-bookrequest')

urlpatterns = [
    path('', include(router.urls)),
]