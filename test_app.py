"""
Test cases for AI Legal Document Assistant
"""

from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from documents.models import Document


class DocumentTestCase(TestCase):
    """Test cases for document functionality."""
    
    def setUp(self):
        """Set up test data."""
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.document = Document.objects.create(
            user=self.user,
            title='Test Document',
            file_type='pdf',
            extracted_text='This is a test legal document.',
            summary='Test summary',
            keywords=['test', 'legal', 'document'],
            is_processed=True
        )
    
    def test_home_page(self):
        """Test home page loads correctly."""
        response = self.client.get(reverse('documents:home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'AI Legal Document Assistant')
    
    def test_upload_page_requires_login(self):
        """Test upload page requires authentication."""
        response = self.client.get(reverse('documents:upload'))
        self.assertEqual(response.status_code, 302)  # Redirect to login
    
    def test_upload_page_with_login(self):
        """Test upload page with authenticated user."""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('documents:upload'))
        self.assertEqual(response.status_code, 200)
    
    def test_document_detail_requires_login(self):
        """Test document detail requires authentication."""
        response = self.client.get(reverse('documents:document_detail', args=[self.document.pk]))
        self.assertEqual(response.status_code, 302)  # Redirect to login
    
    def test_document_detail_with_login(self):
        """Test document detail with authenticated user."""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('documents:document_detail', args=[self.document.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Document')
    
    def test_history_page_requires_login(self):
        """Test history page requires authentication."""
        response = self.client.get(reverse('documents:history'))
        self.assertEqual(response.status_code, 302)  # Redirect to login
    
    def test_history_page_with_login(self):
        """Test history page with authenticated user."""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('documents:history'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Document')
    
    def test_contact_page(self):
        """Test contact page loads correctly."""
        response = self.client.get(reverse('documents:contact'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Contact Us')


class AuthenticationTestCase(TestCase):
    """Test cases for authentication."""
    
    def setUp(self):
        """Set up test data."""
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
    
    def test_login_page(self):
        """Test login page loads correctly."""
        response = self.client.get(reverse('account_login'))
        self.assertEqual(response.status_code, 200)
    
    def test_signup_page(self):
        """Test signup page loads correctly."""
        response = self.client.get(reverse('account_signup'))
        self.assertEqual(response.status_code, 200)
    
    def test_password_reset_page(self):
        """Test password reset page loads correctly."""
        response = self.client.get(reverse('account_reset_password'))
        self.assertEqual(response.status_code, 200)


class ModelTestCase(TestCase):
    """Test cases for models."""
    
    def setUp(self):
        """Set up test data."""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
    
    def test_document_creation(self):
        """Test document model creation."""
        document = Document.objects.create(
            user=self.user,
            title='Test Document',
            file_type='pdf',
            extracted_text='Test content',
            summary='Test summary',
            keywords=['test', 'legal'],
            is_processed=True
        )
        
        self.assertEqual(document.title, 'Test Document')
        self.assertEqual(document.file_type, 'pdf')
        self.assertEqual(document.user, self.user)
        self.assertTrue(document.is_processed)
    
    def test_document_str_representation(self):
        """Test document string representation."""
        document = Document.objects.create(
            user=self.user,
            title='Test Document',
            file_type='pdf'
        )
        
        expected = f"Test Document - {self.user.email}"
        self.assertEqual(str(document), expected)
    
    def test_document_file_size_property(self):
        """Test document file size property."""
        document = Document.objects.create(
            user=self.user,
            title='Test Document',
            file_type='pdf'
        )
        
        # Without actual file, size should be 0
        self.assertEqual(document.file_size, 0)




