from django.utils.deprecation import MiddlewareMixin
from .models import RecentRead

class RecentReadMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # Initialize recent reads tracking in session if not exists
        if 'recent_reads' not in request.session:
            request.session['recent_reads'] = []