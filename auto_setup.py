#!/usr/bin/env python
"""
AI Legal Document Assistant - Automated Setup Script
This script handles all setup automatically without user interaction.
"""

import os
import sys
import subprocess
import django
from pathlib import Path

def run_command(command, description):
    """Run a command and handle errors automatically."""
    print(f"\n🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True, timeout=300)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        if e.stdout:
            print(f"Output: {e.stdout}")
        if e.stderr:
            print(f"Error: {e.stderr}")
        return False
    except subprocess.TimeoutExpired:
        print(f"⏰ {description} timed out")
        return False
    except Exception as e:
        print(f"💥 {description} error: {e}")
        return False

def setup_django():
    """Setup Django environment."""
    print("🚀 Setting up Django environment...")
    
    # Set Django settings
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'legal_assistant.settings')
    
    try:
        django.setup()
        print("✅ Django setup completed")
        return True
    except Exception as e:
        print(f"❌ Django setup failed: {e}")
        return False

def main():
    """Main setup function."""
    print("🎯 AI Legal Document Assistant - Automated Setup")
    print("=" * 60)
    
    # Check if we're in the right directory
    if not os.path.exists('manage.py'):
        print("❌ Error: manage.py not found. Please run this script from the project root directory.")
        return False
    
    # Setup Django first
    if not setup_django():
        print("❌ Django setup failed. Exiting.")
        return False
    
    # Commands to run
    commands = [
        ("python manage.py makemigrations", "Creating migrations"),
        ("python manage.py migrate", "Running migrations"),
        ("python manage.py collectstatic --noinput", "Collecting static files"),
    ]
    
    # Run all commands
    success_count = 0
    for command, description in commands:
        if run_command(command, description):
            success_count += 1
        else:
            print(f"⚠️  Warning: {description} failed, but continuing...")
    
    # Initialize sample data
    print("\n🔄 Initializing sample data...")
    try:
        from django.core.management import call_command
        call_command('init_db')
        print("✅ Sample data initialized")
        success_count += 1
    except Exception as e:
        print(f"⚠️  Warning: Sample data initialization failed: {e}")
    
    # Final status
    print("\n" + "=" * 60)
    print(f"📊 Setup completed: {success_count}/{len(commands) + 1} tasks successful")
    
    if success_count >= len(commands):
        print("🎉 Setup completed successfully!")
        print("\n🚀 To start the server, run:")
        print("   python manage.py runserver")
        print("\n🌐 Then visit: http://127.0.0.1:8000")
        print("\n👤 To create a superuser, run:")
        print("   python manage.py createsuperuser")
        return True
    else:
        print("⚠️  Setup completed with warnings. Some features may not work properly.")
        print("🔧 Check the error messages above for details.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)




