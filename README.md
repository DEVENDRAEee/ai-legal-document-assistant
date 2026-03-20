# AI Legal Document Assistant

A comprehensive Django-based web application that helps legal professionals, students, and the public understand complex legal documents using AI-powered analysis.

## 🎯 Features

- **Document Upload**: Support for PDF, DOCX, JPG, PNG, and TXT files
- **AI Summarization**: Abstractive summarization using Facebook's BART model
- **Keyword Extraction**: Rule-based extraction of legal terms and concepts
- **Semantic Search**: Constitution and IPC section matching using sentence transformers
- **Legal Analysis**: Comprehensive analysis combining summary and legal references
- **User Authentication**: Secure login/registration with Django AllAuth
- **Document History**: Track all processed documents with timestamps
- **Export Options**: Download results in PDF or DOCX format
- **Responsive Design**: Modern UI with Bootstrap 5 and legal-themed styling

## 🏗️ Architecture

- **Backend**: Django 4.2 with SQLite database
- **Frontend**: Bootstrap 5 + Vanilla JavaScript
- **NLP Models**: Hugging Face Transformers and Sentence Transformers
- **Search Engine**: FAISS for semantic search
- **Authentication**: Django AllAuth with email-based login

## 📋 Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- Git

## 🚀 Installation

### 1. Clone the Repository

```bash
git clone <repository-url>
cd ai-legal-document-assistant
```

### 2. Create Virtual Environment

```bash
python -m venv venv
```

### 3. Activate Virtual Environment

**Windows:**
```bash
venv\Scripts\activate
```

**macOS/Linux:**
```bash
source venv/bin/activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Environment Configuration

Copy the example environment file:
```bash
cp env.example .env
```

Edit `.env` file with your configuration:
```env
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

### 6. Database Setup

```bash
python manage.py makemigrations
python manage.py migrate
```

### 7. Create Superuser

```bash
python manage.py createsuperuser
```

### 8. Collect Static Files

```bash
python manage.py collectstatic
```

### 9. Run Development Server

```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000` in your browser.

## 📁 Project Structure

```
ai-legal-document-assistant/
├── legal_assistant/          # Main Django project
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── documents/                # Documents app
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── admin.py
│   └── __init__.py
├── legal_analysis/           # Legal analysis app
│   ├── services.py
│   ├── views.py
│   ├── urls.py
│   ├── admin.py
│   └── __init__.py
├── templates/                # HTML templates
│   ├── base.html
│   └── documents/
│       ├── home.html
│       ├── upload.html
│       ├── document_detail.html
│       ├── history.html
│       └── contact.html
├── static/                   # Static files
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── main.js
├── data/                     # Sample legal data
│   ├── constitution.json
│   └── ipc.json
├── media/                    # Uploaded files
├── manage.py
├── requirements.txt
├── env.example
└── README.md
```

## 🔧 Configuration

### Django Settings

Key settings in `legal_assistant/settings.py`:

- `DEBUG`: Set to `False` in production
- `SECRET_KEY`: Generate a new secret key for production
- `ALLOWED_HOSTS`: Add your domain for production
- `DATABASES`: Configure your production database

### AI Models

The application uses pre-trained models that will be downloaded automatically:

- **Summarization**: `facebook/bart-large-cnn`
- **Semantic Search**: `all-MiniLM-L6-v2`

### Legal Data

Sample legal data is provided in the `data/` directory:

- `constitution.json`: Sample constitutional articles
- `ipc.json`: Sample IPC sections

For production, replace with complete datasets.

## 🎨 Customization

### Styling

The application uses a legal-themed color scheme defined in `static/css/style.css`:

- Primary: Dark blue (`#1e3a8a`)
- Secondary: Gray (`#64748b`)
- Accent: Blue (`#3b82f6`)

### Templates

All templates are located in the `templates/` directory and can be customized to match your branding.

## 🔒 Security Considerations

- Change the `SECRET_KEY` in production
- Set `DEBUG=False` in production
- Use HTTPS in production
- Configure proper database credentials
- Set up proper file upload restrictions
- Implement rate limiting for API endpoints

## 📊 Usage

### For Users

1. **Register/Login**: Create an account or login
2. **Upload Document**: Upload a legal document (PDF, DOCX, etc.)
3. **View Analysis**: Review AI-generated summary, keywords, and legal references
4. **Download Results**: Export analysis in PDF or DOCX format
5. **View History**: Access all previously processed documents

### For Developers

The application provides REST API endpoints for integration:

- `POST /documents/upload/`: Upload and process documents
- `GET /documents/{id}/`: Retrieve document analysis
- `POST /legal/api/search/`: Semantic search API

## 🐛 Troubleshooting

### Common Issues

1. **Import Errors**: Ensure all dependencies are installed
2. **Model Download**: First run may take time to download AI models
3. **File Upload**: Check file size limits and permissions
4. **Database**: Ensure SQLite database is writable

### Debug Mode

Enable debug mode in settings for detailed error messages:

```python
DEBUG = True
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Django framework
- Hugging Face Transformers
- Bootstrap 5
- Font Awesome icons
- Indian Constitution and IPC datasets

## 📞 Support

For support and questions:

- Create an issue on GitHub
- Contact: support@ailegalassistant.com

---

**Note**: This application is for educational and research purposes. Always consult qualified legal professionals for legal advice.
