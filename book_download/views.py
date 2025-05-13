from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.http import FileResponse
from bookAPI.models import Book
from .models import DownloadedBook
from .serializers import DownloadedBookSerializer   
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser  # Optional: limit to admin
from rest_framework import status
from django.shortcuts import get_object_or_404


class DownloadBookView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, book_id):
        try:
            book = Book.objects.get(pk=book_id)
        except Book.DoesNotExist:
            return Response({'error': 'Book not found'}, status=status.HTTP_404_NOT_FOUND)

        if not book.pdf_file:
            return Response({'error': 'PDF not available'}, status=status.HTTP_404_NOT_FOUND)

        # Update or create download record
        download, created = DownloadedBook.objects.get_or_create(
            user=request.user,
            book=book,
            defaults={'download_count': 1}
        )
        
        if not created:
            download.download_count += 1
            download.save()

        # Serve the file
        response = FileResponse(
            book.pdf_file.open(),
            as_attachment=True,
            filename=f"{book.title.replace(' ', '_')}.pdf"
        )
        return response

class UserDownloadsView(generics.ListAPIView):
    serializer_class = DownloadedBookSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return DownloadedBook.objects.filter(user=self.request.user).select_related('book')

class UpdateBookPDFView(APIView):
   # permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]  # 📌 Allow file uploads

    def put(self, request, book_id):
        try:
            book = Book.objects.get(pk=book_id)
        except Book.DoesNotExist:
            return Response({'error': 'Book not found'}, status=status.HTTP_404_NOT_FOUND)

        uploaded_pdf = request.FILES.get('pdf_file')  # Must match Postman key

        if not uploaded_pdf:
            return Response({'error': 'No file uploaded.'}, status=status.HTTP_400_BAD_REQUEST)

        # Replace existing file
        book.pdf_file.save(uploaded_pdf.name, uploaded_pdf, save=True)

        return Response({'message': 'PDF file uploaded/updated successfully.'}, status=status.HTTP_200_OK)
    '''
    if bookAPI.pdf_file:
       bookAPI.pdf_file.delete(save=False)
       bookAPI.pdf_file.save(uploaded_pdf.name, uploaded_pdf, save=True)
'''