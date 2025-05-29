from django.urls import path
from .views import DownloadBookView, UserDownloadsView,UpdateBookPDFView

urlpatterns = [
    path('user/download/<int:book_id>/', DownloadBookView.as_view(), name='download-book'),
    path('user/my-downloads/', UserDownloadsView.as_view(), name='user-downloads'),
    path('admin/update-pdf/<int:book_id>/', UpdateBookPDFView.as_view(), name='update-book-pdf'),
]