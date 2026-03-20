"""
Utility functions for the AI Legal Document Assistant.
"""

import os
import mimetypes
from django.conf import settings
from django.core.files.storage import default_storage


def get_file_type(file_path):
    """Get file type from file path."""
    _, ext = os.path.splitext(file_path)
    return ext.lower().lstrip('.')


def is_allowed_file_type(file_type):
    """Check if file type is allowed."""
    allowed_types = ['pdf', 'docx', 'jpg', 'jpeg', 'png', 'txt']
    return file_type.lower() in allowed_types


def get_file_size_mb(file_size_bytes):
    """Convert file size from bytes to MB."""
    return round(file_size_bytes / (1024 * 1024), 2)


def validate_file_upload(file):
    """Validate uploaded file."""
    errors = []
    
    # Check file size (10MB limit)
    if file.size > 10 * 1024 * 1024:
        errors.append('File size must be less than 10MB.')
    
    # Check file type
    file_type = get_file_type(file.name)
    if not is_allowed_file_type(file_type):
        errors.append('Please upload a PDF, DOCX, JPG, PNG, or TXT file.')
    
    return errors


def get_media_url(file_path):
    """Get media URL for file."""
    if file_path and default_storage.exists(file_path):
        return default_storage.url(file_path)
    return None


def create_directory_if_not_exists(directory_path):
    """Create directory if it doesn't exist."""
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)
        return True
    return False


def get_sample_text():
    """Get sample legal text for testing."""
    return """
    This is a sample legal contract between Party A and Party B. 
    The contract outlines the terms and conditions for the provision of legal services.
    
    Key provisions include:
    1. Scope of services
    2. Payment terms
    3. Confidentiality obligations
    4. Termination clauses
    5. Dispute resolution mechanisms
    
    Both parties agree to be bound by the terms of this agreement and 
    acknowledge that any breach may result in legal consequences under 
    applicable laws and regulations.
    """


def format_legal_score(score):
    """Format legal relevance score for display."""
    if score is None:
        return "N/A"
    return f"{float(score):.2f}"


def truncate_text(text, max_length=200):
    """Truncate text to specified length."""
    if len(text) <= max_length:
        return text
    return text[:max_length] + "..."




