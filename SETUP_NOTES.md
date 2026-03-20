# AI Legal Document Assistant - Setup Notes

## 🚀 Quick Setup Checklist

### 1. Environment Setup
- [ ] Create virtual environment: `python -m venv venv`
- [ ] Activate virtual environment: `venv\Scripts\activate` (Windows) or `source venv/bin/activate` (macOS/Linux)
- [ ] Install dependencies: `pip install -r requirements.txt`

### 2. Django Configuration
- [ ] Run migrations: `python manage.py makemigrations`
- [ ] Apply migrations: `python manage.py migrate`
- [ ] Create superuser: `python manage.py createsuperuser`
- [ ] Collect static files: `python manage.py collectstatic`

### 3. Sample Data
- [ ] Initialize sample data: `python manage.py init_db`
- [ ] Verify data files exist in `data/` directory

### 4. Run Server
- [ ] Start development server: `python manage.py runserver`
- [ ] Visit: http://127.0.0.1:8000

## 🔧 Configuration Notes

### Django AllAuth Setup
The project uses Django AllAuth for authentication. Key settings in `legal_assistant/settings.py`:

```python
# AllAuth configuration
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
```

### File Upload Settings
- Maximum file size: 10MB
- Allowed file types: PDF, DOCX, JPG, PNG, TXT
- Files stored in `media/documents/` directory

### AI Model Configuration
- Summarization model: `facebook/bart-large-cnn`
- Semantic search model: `all-MiniLM-L6-v2`
- Models will be downloaded automatically on first use

## 📁 Directory Structure

```
project/
├── legal_assistant/          # Main Django project
├── documents/               # Documents app
├── legal_analysis/          # NLP processing app
├── templates/               # HTML templates
├── static/                  # CSS, JS, images
├── data/                    # Sample legal data
├── media/                   # Uploaded files
├── manage.py
├── requirements.txt
└── README.md
```

## 🐛 Common Issues & Solutions

### 1. PowerShell Execution Policy Error
**Error**: `ExecutionPolicy` restriction
**Solution**: Use Command Prompt instead of PowerShell, or run:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### 2. Django AllAuth Middleware Error
**Error**: `AccountMiddleware must be added to settings.MIDDLEWARE`
**Solution**: Already fixed in `settings.py` - middleware is properly configured

### 3. Missing Dependencies
**Error**: Import errors for AI libraries
**Solution**: Ensure all packages in `requirements.txt` are installed:
```bash
pip install -r requirements.txt
```

### 4. Database Migration Issues
**Error**: Migration conflicts
**Solution**: Reset migrations if needed:
```bash
python manage.py migrate --fake-initial
```

### 5. Static Files Not Loading
**Error**: CSS/JS files not found
**Solution**: Run collectstatic:
```bash
python manage.py collectstatic
```

## 🔒 Security Considerations

### Production Deployment
- [ ] Change `SECRET_KEY` in settings
- [ ] Set `DEBUG = False`
- [ ] Configure proper database (PostgreSQL recommended)
- [ ] Set up HTTPS/SSL
- [ ] Configure email backend for production
- [ ] Set up proper file storage (AWS S3, etc.)

### Environment Variables
Create `.env` file with:
```env
SECRET_KEY=your-production-secret-key
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
DATABASE_URL=postgresql://user:password@localhost/dbname
```

## 📊 Testing the Application

### 1. Test Installation
```bash
python test_installation.py
```

### 2. Manual Testing Checklist
- [ ] User registration/login works
- [ ] File upload functionality
- [ ] Document processing (AI analysis)
- [ ] Download options (PDF/DOCX)
- [ ] Document history
- [ ] Contact form
- [ ] Responsive design on mobile

### 3. Sample Data Testing
- Demo user: `demo@example.com` / `demo123`
- Sample document available for testing

## 🚀 Deployment Options

### 1. Local Development
- Use SQLite database
- Run with `python manage.py runserver`
- Access at `http://127.0.0.1:8000`

### 2. Production Deployment
- Use PostgreSQL database
- Deploy with Gunicorn + Nginx
- Use environment variables for configuration
- Set up proper static file serving

### 3. Cloud Deployment
- Heroku: Use `Procfile` and `runtime.txt`
- AWS: Use Elastic Beanstalk or EC2
- DigitalOcean: Use App Platform

## 📝 Additional Features to Implement

### Future Enhancements
- [ ] User profile management
- [ ] Document sharing capabilities
- [ ] Advanced search filters
- [ ] Batch document processing
- [ ] API rate limiting
- [ ] Document versioning
- [ ] Advanced analytics dashboard
- [ ] Integration with legal databases
- [ ] Multi-language support

### Performance Optimizations
- [ ] Implement caching (Redis)
- [ ] Optimize database queries
- [ ] Add pagination for large datasets
- [ ] Implement background task processing (Celery)
- [ ] Add CDN for static files

## 🆘 Support & Troubleshooting

### Getting Help
1. Check the README.md file
2. Run `python test_installation.py`
3. Check Django logs for errors
4. Verify all dependencies are installed
5. Ensure database migrations are applied

### Log Files
- Django logs: Check console output
- Error logs: Check browser developer tools
- File upload logs: Check `media/` directory permissions

---

**Note**: This application is designed for educational and research purposes. Always consult qualified legal professionals for actual legal advice.
