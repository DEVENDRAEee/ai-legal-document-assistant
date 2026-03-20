# AI Legal Document Assistant - Docker Configuration

## 🐳 Docker Setup

This document provides Docker configuration for the AI Legal Document Assistant.

## 📁 Docker Files

### Dockerfile
```dockerfile
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        postgresql-client \
        tesseract-ocr \
        libtesseract-dev \
        poppler-utils \
        libmagic1 \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . /app/

# Create directories
RUN mkdir -p /app/media /app/staticfiles

# Collect static files
RUN python manage.py collectstatic --noinput

# Expose port
EXPOSE 8000

# Run the application
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "legal_assistant.wsgi:application"]
```

### docker-compose.yml
```yaml
version: '3.8'

services:
  db:
    image: postgres:15
    volumes:
      - postgres_data:/var/lib/postgresql/data/
    environment:
      - POSTGRES_DB=legal_assistant
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=postgres
    ports:
      - "5432:5432"

  web:
    build: .
    command: >
      sh -c "python manage.py migrate &&
             python manage.py init_db &&
             gunicorn legal_assistant.wsgi:application --bind 0.0.0.0:8000"
    volumes:
      - .:/app
      - media_files:/app/media
    ports:
      - "8000:8000"
    environment:
      - DEBUG=False
      - SECRET_KEY=your-production-secret-key
      - DATABASE_URL=postgresql://postgres:postgres@db:5432/legal_assistant
    depends_on:
      - db

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - media_files:/app/media
      - static_files:/app/staticfiles
    depends_on:
      - web

volumes:
  postgres_data:
  media_files:
  static_files:
```

### nginx.conf
```nginx
events {
    worker_connections 1024;
}

http {
    upstream web {
        server web:8000;
    }

    server {
        listen 80;
        server_name localhost;

        location / {
            proxy_pass http://web;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }

        location /static/ {
            alias /app/staticfiles/;
        }

        location /media/ {
            alias /app/media/;
        }
    }
}
```

### .dockerignore
```
__pycache__
*.pyc
*.pyo
*.pyd
.Python
env
pip-log.txt
pip-delete-this-directory.txt
.tox
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
*.log
.git
.mypy_cache
.pytest_cache
.hypothesis

.DS_Store
.vscode
.idea
*.swp
*.swo

node_modules
npm-debug.log

venv/
.venv/
ENV/
env.bak/
venv.bak/

*.sqlite3
db.sqlite3
media/
staticfiles/
```

## 🚀 Docker Commands

### Build and Run
```bash
# Build the image
docker build -t ai-legal-assistant .

# Run with docker-compose
docker-compose up --build

# Run in background
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### Development
```bash
# Run with volume mounting for development
docker-compose -f docker-compose.dev.yml up

# Access container shell
docker-compose exec web bash

# Run Django commands
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
docker-compose exec web python manage.py init_db
```

### Production
```bash
# Build for production
docker-compose -f docker-compose.prod.yml up --build

# Scale services
docker-compose up --scale web=3

# Update services
docker-compose pull
docker-compose up -d
```

## 🔧 Environment Variables

### Development (.env.dev)
```env
DEBUG=True
SECRET_KEY=dev-secret-key
DATABASE_URL=postgresql://postgres:postgres@db:5432/legal_assistant
ALLOWED_HOSTS=localhost,127.0.0.1
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
```

### Production (.env.prod)
```env
DEBUG=False
SECRET_KEY=your-production-secret-key
DATABASE_URL=postgresql://user:password@db:5432/legal_assistant
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

## 📊 Docker Health Checks

### Health Check Script
```bash
#!/bin/bash
# healthcheck.sh

# Check if Django is running
curl -f http://localhost:8000/health/ || exit 1

# Check database connection
python manage.py check --database default || exit 1

exit 0
```

### Dockerfile with Health Check
```dockerfile
# Add to Dockerfile
COPY healthcheck.sh /app/
RUN chmod +x /app/healthcheck.sh

HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD /app/healthcheck.sh
```

## 🐳 Docker Compose Variations

### Development (docker-compose.dev.yml)
```yaml
version: '3.8'

services:
  db:
    image: postgres:15
    environment:
      - POSTGRES_DB=legal_assistant
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=postgres
    ports:
      - "5432:5432"

  web:
    build: .
    command: python manage.py runserver 0.0.0.0:8000
    volumes:
      - .:/app
    ports:
      - "8000:8000"
    environment:
      - DEBUG=True
      - SECRET_KEY=dev-secret-key
      - DATABASE_URL=postgresql://postgres:postgres@db:5432/legal_assistant
    depends_on:
      - db
```

### Production (docker-compose.prod.yml)
```yaml
version: '3.8'

services:
  db:
    image: postgres:15
    volumes:
      - postgres_data:/var/lib/postgresql/data/
    environment:
      - POSTGRES_DB=legal_assistant
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=postgres
    restart: unless-stopped

  web:
    build: .
    command: >
      sh -c "python manage.py migrate &&
             python manage.py collectstatic --noinput &&
             gunicorn legal_assistant.wsgi:application --bind 0.0.0.0:8000"
    volumes:
      - media_files:/app/media
      - static_files:/app/staticfiles
    environment:
      - DEBUG=False
      - SECRET_KEY=your-production-secret-key
      - DATABASE_URL=postgresql://postgres:postgres@db:5432/legal_assistant
    depends_on:
      - db
    restart: unless-stopped

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.prod.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/nginx/ssl
      - media_files:/app/media
      - static_files:/app/staticfiles
    depends_on:
      - web
    restart: unless-stopped

volumes:
  postgres_data:
  media_files:
  static_files:
```

## 🔒 Security Considerations

### Docker Security
- Use non-root user in container
- Keep base images updated
- Scan images for vulnerabilities
- Use secrets management
- Limit container privileges

### Example Secure Dockerfile
```dockerfile
FROM python:3.11-slim

# Create non-root user
RUN groupadd -r django && useradd -r -g django django

# Install dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    postgresql-client tesseract-ocr && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

# Change ownership
RUN chown -R django:django /app

# Switch to non-root user
USER django

# Expose port
EXPOSE 8000

# Run application
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "legal_assistant.wsgi:application"]
```

## 📈 Monitoring and Logging

### Logging Configuration
```python
# settings.py
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
            'level': 'INFO',
        },
    },
}
```

### Docker Logging
```yaml
# docker-compose.yml
services:
  web:
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"
```

## 🚀 Deployment with Docker

### Docker Hub
```bash
# Build and tag
docker build -t your-username/ai-legal-assistant:latest .

# Push to Docker Hub
docker push your-username/ai-legal-assistant:latest
```

### Kubernetes
```yaml
# k8s-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ai-legal-assistant
spec:
  replicas: 3
  selector:
    matchLabels:
      app: ai-legal-assistant
  template:
    metadata:
      labels:
        app: ai-legal-assistant
    spec:
      containers:
      - name: web
        image: your-username/ai-legal-assistant:latest
        ports:
        - containerPort: 8000
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: db-secret
              key: url
```

---

For more information, see the main [README.md](README.md) and [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) files.




