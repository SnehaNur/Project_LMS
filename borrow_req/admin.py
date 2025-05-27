from django.contrib import admin
from .models import BookAvailability

@admin.register(BookAvailability)
class BookAvailabilityAdmin(admin.ModelAdmin):
    list_display = ('book', 'total_copies', 'available_copies')
    list_filter = ('book',)
    search_fields = ('book__title',)
