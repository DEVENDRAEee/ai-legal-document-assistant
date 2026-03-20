"""
Script to reprocess all documents in the database with the updated processor.
This will extract keywords, constitutional references, IPC sections, and generate proper analysis.
"""

import os
import sys
import django

# Setup Django
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'legal_assistant.settings')
django.setup()

from documents.models import Document
from legal_analysis.services import DocumentProcessor

def reprocess_documents():
    """Reprocess all documents in the database."""
    print("Reprocessing all documents...")
    print("=" * 60)
    
    documents = Document.objects.all()
    
    if not documents.exists():
        print("No documents found in database.")
        return
    
    print(f"Found {documents.count()} document(s) to process\n")
    
    processor = DocumentProcessor()
    
    success_count = 0
    fail_count = 0
    
    for doc in documents:
        try:
            print(f"Processing: {doc.title}")
            print(f"  File: {doc.file_type}")
            print(f"  Current status: {'Processed' if doc.is_processed else 'Not Processed'}")
            
            # Process the document
            result = processor.process_document(doc)
            
            # Update document with results
            doc.extracted_text = result.get('extracted_text', '')
            doc.summary = result.get('summary', '')
            doc.keywords = result.get('keywords', [])
            doc.constitutional_references = result.get('constitutional_references', [])
            doc.ipc_sections = result.get('ipc_sections', [])
            doc.legal_analysis = result.get('legal_analysis', '')
            doc.is_processed = True
            doc.processing_error = None
            doc.save()
            
            # Display results
            print(f"  ✓ Success!")
            print(f"    - Extracted text: {len(result.get('extracted_text', ''))} chars")
            print(f"    - Summary: {len(result.get('summary', ''))} chars")
            print(f"    - Keywords: {len(result.get('keywords', []))} keywords")
            if result.get('keywords'):
                print(f"    - Keywords list: {result.get('keywords', [])[:5]}")
            print(f"    - Constitutional references: {len(result.get('constitutional_references', []))}")
            print(f"    - IPC sections: {len(result.get('ipc_sections', []))}")
            print(f"    - Legal analysis: {len(result.get('legal_analysis', ''))} chars")
            
            success_count += 1
            
        except Exception as e:
            print(f"  ✗ Failed: {str(e)}")
            doc.processing_error = str(e)
            doc.save()
            fail_count += 1
        
        print()
    
    print("=" * 60)
    print(f"Processing complete!")
    print(f"Success: {success_count}")
    print(f"Failed: {fail_count}")
    print("=" * 60)

if __name__ == '__main__':
    reprocess_documents()



