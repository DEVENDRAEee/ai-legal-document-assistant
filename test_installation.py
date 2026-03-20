"""
Test script to verify AI Legal Document Assistant installation
"""

import os
import sys
import django

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'legal_assistant.settings')
django.setup()

def test_imports():
    """Test if all required modules can be imported."""
    print("Testing imports...")
    
    try:
        import django
        print(f"✓ Django {django.get_version()}")
    except ImportError as e:
        print(f"✗ Django import failed: {e}")
        return False
    
    try:
        from documents.models import Document
        print("✓ Documents models imported")
    except ImportError as e:
        print(f"✗ Documents models import failed: {e}")
        return False
    
    try:
        from legal_analysis.services import DocumentProcessor
        print("✓ Legal analysis services imported")
    except ImportError as e:
        print(f"✗ Legal analysis services import failed: {e}")
        return False
    
    try:
        import transformers
        print("✓ Transformers library imported")
    except ImportError as e:
        print(f"✗ Transformers import failed: {e}")
        return False
    
    try:
        import sentence_transformers
        print("✓ Sentence Transformers imported")
    except ImportError as e:
        print(f"✗ Sentence Transformers import failed: {e}")
        return False
    
    try:
        import faiss
        print("✓ FAISS imported")
    except ImportError as e:
        print(f"✗ FAISS import failed: {e}")
        return False
    
    return True

def test_database():
    """Test database connectivity."""
    print("\nTesting database...")
    
    try:
        from django.db import connection
        cursor = connection.cursor()
        cursor.execute("SELECT 1")
        print("✓ Database connection successful")
        return True
    except Exception as e:
        print(f"✗ Database connection failed: {e}")
        return False

def test_models():
    """Test model creation."""
    print("\nTesting models...")
    
    try:
        from documents.models import Document
        from django.contrib.auth.models import User
        
        # Test model creation
        user_count = User.objects.count()
        doc_count = Document.objects.count()
        
        print(f"✓ Users in database: {user_count}")
        print(f"✓ Documents in database: {doc_count}")
        return True
    except Exception as e:
        print(f"✗ Model test failed: {e}")
        return False

def test_data_files():
    """Test if sample data files exist."""
    print("\nTesting data files...")
    
    data_files = [
        'data/constitution.json',
        'data/ipc.json'
    ]
    
    all_exist = True
    for file_path in data_files:
        if os.path.exists(file_path):
            print(f"✓ {file_path} exists")
        else:
            print(f"✗ {file_path} missing")
            all_exist = False
    
    return all_exist

def main():
    """Run all tests."""
    print("AI Legal Document Assistant - Installation Test")
    print("=" * 50)
    
    tests = [
        test_imports,
        test_database,
        test_models,
        test_data_files
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print("\n" + "=" * 50)
    print(f"Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("✓ All tests passed! Installation is successful.")
        print("\nNext steps:")
        print("1. Run: python manage.py runserver")
        print("2. Visit: http://127.0.0.1:8000")
        print("3. Create a superuser: python manage.py createsuperuser")
        print("4. Initialize sample data: python manage.py init_db")
    else:
        print("✗ Some tests failed. Please check the installation.")
        print("\nTroubleshooting:")
        print("1. Make sure all dependencies are installed: pip install -r requirements.txt")
        print("2. Run migrations: python manage.py migrate")
        print("3. Check Django settings: legal_assistant/settings.py")

if __name__ == "__main__":
    main()
