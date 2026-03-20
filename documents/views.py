from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView, ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse, HttpResponse
from django.contrib import messages
from django.core.files.storage import default_storage
from django.conf import settings
import os
import json
from .models import Document
from legal_analysis.services import DocumentProcessor


class HomeView(TemplateView):
    """Home page view."""
    template_name = 'documents/home.html'


class UploadView(LoginRequiredMixin, TemplateView):
    """Document upload page."""
    template_name = 'documents/upload.html'
    
    def post(self, request, *args, **kwargs):
        """Handle file upload."""
        try:
            file = request.FILES.get('file')
            title = request.POST.get('title', '')
            
            if not file:
                return JsonResponse({'success': False, 'message': 'No file provided'})
            
            if not title:
                title = file.name
            
            # Create document record
            document = Document.objects.create(
                user=request.user,
                title=title,
                file=file,
                file_type=file.name.split('.')[-1].lower()
            )
            
            # Process the document immediately
            try:
                processor = DocumentProcessor()
                result = processor.process_document(document)
                
                # Update document with results
                document.extracted_text = result.get('extracted_text', '')
                document.summary = result.get('summary', '')
                document.keywords = result.get('keywords', [])
                document.constitutional_references = result.get('constitutional_references', [])
                document.ipc_sections = result.get('ipc_sections', [])
                document.legal_analysis = result.get('legal_analysis', '')
                document.is_processed = True
                document.save()
                
            except Exception as e:
                document.processing_error = str(e)
                document.save()
            
            return JsonResponse({
                'success': True,
                'message': 'File uploaded and processed successfully',
                'redirect_url': f'/document/{document.pk}/'
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': f'Error uploading file: {str(e)}'
            })


class DocumentDetailView(LoginRequiredMixin, DetailView):
    """Document detail and results page."""
    model = Document
    template_name = 'documents/document_detail.html'
    context_object_name = 'document'
    
    def get_queryset(self):
        return Document.objects.filter(user=self.request.user)


class HistoryView(LoginRequiredMixin, ListView):
    """User's document history."""
    model = Document
    template_name = 'documents/history.html'
    context_object_name = 'documents'
    paginate_by = 10
    
    def get_queryset(self):
        return Document.objects.filter(user=self.request.user)


class ContactView(TemplateView):
    """Contact page."""
    template_name = 'documents/contact.html'


class FAQView(TemplateView):
    """FAQ page."""
    template_name = 'documents/faq.html'


class ProcessDocumentView(LoginRequiredMixin, DetailView):
    """Process uploaded document."""
    model = Document
    
    def get_queryset(self):
        return Document.objects.filter(user=self.request.user)
    
    def post(self, request, *args, **kwargs):
        document = self.get_object()
        
        try:
            processor = DocumentProcessor()
            result = processor.process_document(document)
            
            # Update document with results
            document.extracted_text = result.get('extracted_text', '')
            document.summary = result.get('summary', '')
            document.keywords = result.get('keywords', [])
            document.constitutional_references = result.get('constitutional_references', [])
            document.ipc_sections = result.get('ipc_sections', [])
            document.legal_analysis = result.get('legal_analysis', '')
            document.is_processed = True
            document.save()
            
            return JsonResponse({
                'success': True,
                'message': 'Document processed successfully',
                'redirect_url': f'/document/{document.pk}/'
            })
            
        except Exception as e:
            document.processing_error = str(e)
            document.save()
            
            return JsonResponse({
                'success': False,
                'message': f'Error processing document: {str(e)}'
            })


class DownloadView(LoginRequiredMixin, DetailView):
    """Download processed document in various formats."""
    model = Document
    
    def get_queryset(self):
        return Document.objects.filter(user=self.request.user)
    
    def get(self, request, *args, **kwargs):
        document = self.get_object()
        format_type = kwargs.get('format')
        
        if not document.is_processed:
            messages.error(request, 'Document has not been processed yet.')
            return redirect('documents:document_detail', pk=document.pk)
        
        try:
            from legal_analysis.services import DocumentExporter
            exporter = DocumentExporter()
            
            if format_type == 'pdf':
                response = exporter.export_to_pdf(document)
                response['Content-Disposition'] = f'attachment; filename="{document.title}_analysis.pdf"'
                return response
            elif format_type == 'docx':
                response = exporter.export_to_docx(document)
                response['Content-Disposition'] = f'attachment; filename="{document.title}_analysis.docx"'
                return response
            else:
                messages.error(request, 'Invalid format specified.')
                return redirect('documents:document_detail', pk=document.pk)
                
        except Exception as e:
            messages.error(request, f'Error generating download: {str(e)}')
            return redirect('documents:document_detail', pk=document.pk)
