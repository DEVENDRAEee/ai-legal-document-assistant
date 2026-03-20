from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Document(models.Model):
    """Model to store uploaded documents and their analysis results."""
    
    DOCUMENT_TYPES = [
        ('pdf', 'PDF'),
        ('docx', 'DOCX'),
        ('jpg', 'JPG'),
        ('png', 'PNG'),
        ('txt', 'TXT'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='documents')
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to='documents/')
    file_type = models.CharField(max_length=10, choices=DOCUMENT_TYPES)
    uploaded_at = models.DateTimeField(default=timezone.now)
    
    # Extracted content
    extracted_text = models.TextField(blank=True, null=True)
    
    # Analysis results
    summary = models.TextField(blank=True, null=True)
    keywords = models.JSONField(default=list, blank=True)
    constitutional_references = models.JSONField(default=list, blank=True)
    ipc_sections = models.JSONField(default=list, blank=True)
    legal_analysis = models.TextField(blank=True, null=True)
    
    # Processing status
    is_processed = models.BooleanField(default=False)
    processing_error = models.TextField(blank=True, null=True)
    
    class Meta:
        ordering = ['-uploaded_at']
    
    def __str__(self):
        return f"{self.title} - {self.user.email}"
    
    @property
    def file_size(self):
        """Return file size in MB."""
        if self.file:
            return round(self.file.size / (1024 * 1024), 2)
        return 0




