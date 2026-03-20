# AI Legal Document Assistant - Troubleshooting Guide

## 🔧 Common Issues & Solutions

### Installation Issues

#### 1. Python Version Error
**Error**: `Python 3.8+ is required`
**Solution**:
```bash
# Check Python version
python --version

# Install Python 3.11 if needed
# Windows: Download from python.org
# macOS: brew install python@3.11
# Ubuntu: sudo apt install python3.11
```

#### 2. Virtual Environment Issues
**Error**: `venv\Scripts\activate` not working
**Solution**:
```bash
# Use Command Prompt instead of PowerShell
cmd /c "venv\Scripts\activate.bat"

# Or fix PowerShell execution policy
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

#### 3. Dependencies Installation Failed
**Error**: `pip install` fails
**Solution**:
```bash
# Upgrade pip first
python -m pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt

# If specific package fails, install individually
pip install Django==4.2.7
pip install django-allauth==0.57.0
```

#### 4. Database Migration Errors
**Error**: `django.db.utils.OperationalError`
**Solution**:
```bash
# Delete existing database
rm db.sqlite3

# Run migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser
```

### Runtime Issues

#### 1. Server Won't Start
**Error**: `ModuleNotFoundError` or import errors
**Solution**:
```bash
# Activate virtual environment
venv\Scripts\activate  # Windows
source venv/bin/activate  # macOS/Linux

# Check if all packages are installed
pip list

# Reinstall requirements
pip install -r requirements.txt

# Run server
python manage.py runserver
```

#### 2. Static Files Not Loading
**Error**: CSS/JS files return 404
**Solution**:
```bash
# Collect static files
python manage.py collectstatic

# Check STATIC_URL in settings.py
# Ensure static files are in correct directory
```

#### 3. File Upload Issues
**Error**: File upload fails or times out
**Solution**:
- Check file size (must be < 10MB)
- Verify file format (PDF, DOCX, JPG, PNG, TXT)
- Check MEDIA_ROOT permissions
- Ensure sufficient disk space

#### 4. AI Model Loading Errors
**Error**: `OSError: [Errno 2] No such file or directory`
**Solution**:
```bash
# Models download automatically on first use
# Ensure internet connection
# Check disk space (models are large)
# Try running with smaller document first
```

### Authentication Issues

#### 1. Login/Registration Not Working
**Error**: Forms not submitting or validation errors
**Solution**:
- Check CSRF token in forms
- Verify email backend configuration
- Check ALLOWED_HOSTS in settings
- Clear browser cache and cookies

#### 2. Email Verification Issues
**Error**: Email verification emails not sent
**Solution**:
```python
# In settings.py, configure email backend
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'  # For development
# Check console for email content
```

#### 3. Password Reset Not Working
**Error**: Password reset emails not received
**Solution**:
- Check email configuration
- Verify SMTP settings
- Check spam folder
- Use console email backend for testing

### Performance Issues

#### 1. Slow Document Processing
**Symptoms**: Processing takes too long
**Solution**:
- Check document size (should be < 10MB)
- Verify internet connection (needed for AI models)
- Check server resources (CPU, memory)
- Try with smaller document first
- Consider upgrading server specs

#### 2. High Memory Usage
**Symptoms**: Application uses too much RAM
**Solution**:
- Close other applications
- Increase virtual memory
- Consider using smaller AI models
- Implement model caching

#### 3. Database Performance Issues
**Symptoms**: Slow queries, timeouts
**Solution**:
```bash
# Optimize database
python manage.py dbshell
# Run VACUUM; ANALYZE; in SQLite

# For production, use PostgreSQL
# Add database indexes
# Implement connection pooling
```

### AI Processing Issues

#### 1. Text Extraction Failed
**Error**: No text extracted from document
**Solution**:
- Check if document is corrupted
- Verify file format is supported
- Try with different document
- Check OCR dependencies (Tesseract)

#### 2. Summarization Errors
**Error**: AI summarization fails
**Solution**:
- Check internet connection
- Verify Hugging Face model access
- Try with shorter document
- Check available memory

#### 3. Search Results Empty
**Error**: No constitutional or IPC references found
**Solution**:
- Check if sample data files exist
- Verify data file format
- Try with different document content
- Check search algorithm parameters

### Browser Issues

#### 1. JavaScript Not Working
**Symptoms**: Interactive features don't work
**Solution**:
- Check browser console for errors
- Verify JavaScript is enabled
- Clear browser cache
- Try different browser
- Check if Bootstrap JS is loaded

#### 2. CSS Not Loading
**Symptoms**: Page looks unstyled
**Solution**:
- Check if CSS files are accessible
- Verify STATIC_URL configuration
- Run collectstatic command
- Check file permissions

#### 3. Mobile Display Issues
**Symptoms**: Layout broken on mobile
**Solution**:
- Check viewport meta tag
- Verify Bootstrap responsive classes
- Test on different screen sizes
- Check CSS media queries

### Production Deployment Issues

#### 1. Static Files Not Served
**Error**: 404 for static files in production
**Solution**:
```python
# Configure static file serving
STATIC_ROOT = '/path/to/staticfiles'
STATIC_URL = '/static/'

# Use whitenoise for serving static files
MIDDLEWARE = [
    'whitenoise.middleware.WhiteNoiseMiddleware',
    # ... other middleware
]
```

#### 2. Database Connection Errors
**Error**: Database connection failed
**Solution**:
- Check database credentials
- Verify database server is running
- Check network connectivity
- Verify database permissions

#### 3. SSL/HTTPS Issues
**Error**: Mixed content or SSL errors
**Solution**:
- Configure HTTPS properly
- Update ALLOWED_HOSTS
- Use secure cookies
- Check certificate validity

### Debugging Steps

#### 1. Enable Debug Mode
```python
# In settings.py
DEBUG = True
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
    },
}
```

#### 2. Check Logs
```bash
# Django logs
python manage.py runserver --verbosity=2

# Check browser console for JavaScript errors
# Check server logs for Python errors
# Check database logs for SQL errors
```

#### 3. Test Installation
```bash
# Run installation test
python test_installation.py

# Check specific components
python manage.py check
python manage.py check --deploy
```

#### 4. Verify Dependencies
```bash
# Check installed packages
pip list

# Check for conflicts
pip check

# Update packages
pip install --upgrade -r requirements.txt
```

### Getting Help

#### 1. Check Documentation
- README.md - Project overview
- SETUP_NOTES.md - Detailed setup instructions
- FAQ.md - Frequently asked questions
- API_DOCUMENTATION.md - API reference

#### 2. Run Diagnostic Scripts
```bash
# Test installation
python test_installation.py

# Check Django configuration
python manage.py check

# Test database
python manage.py dbshell
```

#### 3. Contact Support
- Create GitHub issue with detailed error information
- Include error logs and system information
- Provide steps to reproduce the issue
- Check existing issues for similar problems

#### 4. Community Help
- GitHub Discussions
- Stack Overflow (tag: django, ai-legal-assistant)
- Django Community Forum

### Prevention Tips

#### 1. Regular Maintenance
- Keep dependencies updated
- Monitor disk space
- Check logs regularly
- Backup database regularly

#### 2. Performance Monitoring
- Monitor memory usage
- Check response times
- Monitor error rates
- Set up alerts for critical issues

#### 3. Security Best Practices
- Keep Django updated
- Use strong passwords
- Enable HTTPS in production
- Regular security audits

---

## 🆘 Emergency Recovery

### Complete Reset
```bash
# Stop server
# Delete database
rm db.sqlite3

# Recreate virtual environment
rm -rf venv
python -m venv venv
venv\Scripts\activate

# Reinstall everything
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py init_db
python manage.py runserver
```

### Data Recovery
```bash
# If you have database backup
cp backup.db.sqlite3 db.sqlite3

# If you have media files backup
cp -r backup_media/* media/

# Run migrations
python manage.py migrate
```

---

*This troubleshooting guide is regularly updated. For the latest version, check the GitHub repository.*




