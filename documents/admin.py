from django.contrib import admin
from .models import Document


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'file_type', 'uploaded_at', 'is_processed']
    list_filter = ['file_type', 'is_processed', 'uploaded_at']
    search_fields = ['title', 'user__email']
    readonly_fields = ['uploaded_at', 'file_size']
    
    def file_size(self, obj):
        return f"{obj.file_size} MB"
    file_size.short_description = 'File Size'




