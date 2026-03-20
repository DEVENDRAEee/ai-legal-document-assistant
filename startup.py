#!/usr/bin/env python
"""
AI Legal Document Assistant - Startup Script
"""

import os
import sys
import subprocess
import django

def run_command(command, description):
    """Run a command and handle errors."""
    print(f"\n{description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✓ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ {description} failed: {e}")
        print(f"Error output: {e.stderr}")
        return False

def main():
    """Main startup function."""
    print("AI Legal Document Assistant - Startup Script")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not os.path.exists('manage.py'):
        print("✗ Error: manage.py not found. Please run this script from the project root directory.")
        return False
    
    # Set up Django
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'legal_assistant.settings')
    
    try:
        django.setup()
        print("✓ Django setup completed")
    except Exception as e:
        print(f"✗ Django setup failed: {e}")
        return False
    
    # Run startup commands
    commands = [
        ("python manage.py makemigrations", "Creating migrations"),
        ("python manage.py migrate", "Running migrations"),
        ("python manage.py collectstatic --noinput", "Collecting static files"),
    ]
    
    for command, description in commands:
        if not run_command(command, description):
            print(f"\n⚠️  Warning: {description} failed, but continuing...")
    
    # Initialize sample data
    print("\nInitializing sample data...")
    try:
        from django.core.management import call_command
        call_command('init_db')
        print("✓ Sample data initialized")
    except Exception as e:
        print(f"⚠️  Warning: Sample data initialization failed: {e}")
    
    print("\n" + "=" * 50)
    print("✓ Startup completed successfully!")
    print("\nTo start the development server, run:")
    print("python manage.py runserver")
    print("\nThen visit: http://127.0.0.1:8000")
    print("\nTo create a superuser, run:")
    print("python manage.py createsuperuser")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
