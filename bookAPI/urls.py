from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from .views import BookViewSet, CategoryViewSet,BookSearchView,ReadBooksView,MarkAsReadView

router = DefaultRouter()
router.register(r'books', BookViewSet, basename='book')
router.register(r'categories', CategoryViewSet, basename='category')

urlpatterns = [
    path('', include(router.urls)),
    path('book_search/', BookSearchView.as_view(), name='book-search'),
    path('user/read-books/', ReadBooksView.as_view(), name='user-read-books'), # for see the readed books
    path('books/<int:pk>/mark_as_read/', MarkAsReadView.as_view(), name='book-mark-as-read'),
    #path('book_search/<str:query>/', BookViewSet.as_view({'get': 'list'}), name='book-search'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)