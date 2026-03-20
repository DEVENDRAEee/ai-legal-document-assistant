# AI Legal Document Assistant - Deployment Guide

## 🚀 Production Deployment Options

### 1. Heroku Deployment

#### Prerequisites
- Heroku CLI installed
- Git repository
- Heroku account

#### Steps
1. **Create Heroku App**
   ```bash
   heroku create your-app-name
   ```

2. **Set Environment Variables**
   ```bash
   heroku config:set SECRET_KEY=your-production-secret-key
   heroku config:set DEBUG=False
   heroku config:set ALLOWED_HOSTS=your-app-name.herokuapp.com
   ```

3. **Configure Database**
   ```bash
   heroku addons:create heroku-postgresql:hobby-dev
   ```

4. **Deploy**
   ```bash
   git add .
   git commit -m "Deploy to Heroku"
   git push heroku main
   ```

5. **Run Migrations**
   ```bash
   heroku run python manage.py migrate
   heroku run python manage.py createsuperuser
   ```

### 2. AWS Elastic Beanstalk

#### Prerequisites
- AWS CLI installed
- EB CLI installed
- AWS account

#### Steps
1. **Initialize EB Application**
   ```bash
   eb init
   eb create production
   ```

2. **Configure Environment Variables**
   ```bash
   eb setenv SECRET_KEY=your-production-secret-key
   eb setenv DEBUG=False
   eb setenv ALLOWED_HOSTS=your-app.elasticbeanstalk.com
   ```

3. **Deploy**
   ```bash
   eb deploy
   ```

### 3. DigitalOcean App Platform

#### Steps
1. **Create App Spec File**
   ```yaml
   name: ai-legal-assistant
   services:
   - name: web
     source_dir: /
     github:
       repo: your-username/ai-legal-assistant
       branch: main
     run_command: gunicorn legal_assistant.wsgi:application
     environment_slug: python
     instance_count: 1
     instance_size_slug: basic-xxs
     envs:
     - key: SECRET_KEY
       value: your-production-secret-key
     - key: DEBUG
       value: "False"
     - key: ALLOWED_HOSTS
       value: your-app.ondigitalocean.app
   ```

2. **Deploy via DigitalOcean Dashboard**

### 4. VPS Deployment (Ubuntu/CentOS)

#### Prerequisites
- Ubuntu 20.04+ or CentOS 8+
- Python 3.8+
- Nginx
- PostgreSQL

#### Steps
1. **Install Dependencies**
   ```bash
   sudo apt update
   sudo apt install python3-pip python3-venv nginx postgresql postgresql-contrib
   ```

2. **Create Application User**
   ```bash
   sudo adduser --system --group --shell /bin/bash django
   ```

3. **Clone Repository**
   ```bash
   cd /home/django
   git clone https://github.com/your-username/ai-legal-assistant.git
   cd ai-legal-assistant
   ```

4. **Setup Virtual Environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

5. **Configure Database**
   ```bash
   sudo -u postgres psql
   CREATE DATABASE legal_assistant;
   CREATE USER django WITH PASSWORD 'your-password';
   GRANT ALL PRIVILEGES ON DATABASE legal_assistant TO django;
   \q
   ```

6. **Configure Django Settings**
   ```python
   # settings.py
   DEBUG = False
   ALLOWED_HOSTS = ['your-domain.com', 'www.your-domain.com']
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.postgresql',
           'NAME': 'legal_assistant',
           'USER': 'django',
           'PASSWORD': 'your-password',
           'HOST': 'localhost',
           'PORT': '5432',
       }
   }
   ```

7. **Run Migrations**
   ```bash
   python manage.py migrate
   python manage.py collectstatic
   python manage.py createsuperuser
   ```

8. **Configure Gunicorn**
   ```bash
   pip install gunicorn
   gunicorn --bind 0.0.0.0:8000 legal_assistant.wsgi:application
   ```

9. **Configure Nginx**
   ```nginx
   server {
       listen 80;
       server_name your-domain.com www.your-domain.com;
       
       location / {
           proxy_pass http://127.0.0.1:8000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
           proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
           proxy_set_header X-Forwarded-Proto $scheme;
       }
       
       location /static/ {
           alias /home/django/ai-legal-assistant/staticfiles/;
       }
       
       location /media/ {
           alias /home/django/ai-legal-assistant/media/;
       }
   }
   ```

10. **Setup Systemd Service**
    ```ini
    [Unit]
    Description=AI Legal Document Assistant
    After=network.target

    [Service]
    User=django
    Group=django
    WorkingDirectory=/home/django/ai-legal-assistant
    Environment="PATH=/home/django/ai-legal-assistant/venv/bin"
    ExecStart=/home/django/ai-legal-assistant/venv/bin/gunicorn --workers 3 --bind unix:/home/django/ai-legal-assistant/legal_assistant.sock legal_assistant.wsgi:application

    [Install]
    WantedBy=multi-user.target
    ```

## 🔒 Security Configuration

### 1. Environment Variables
```bash
# Production settings
SECRET_KEY=your-very-secure-secret-key-here
DEBUG=False
ALLOWED_HOSTS=your-domain.com,www.your-domain.com
DATABASE_URL=postgresql://user:password@localhost/dbname
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

### 2. SSL/HTTPS Setup
```bash
# Install Certbot
sudo apt install certbot python3-certbot-nginx

# Get SSL certificate
sudo certbot --nginx -d your-domain.com -d www.your-domain.com
```

### 3. Firewall Configuration
```bash
# UFW setup
sudo ufw allow 22
sudo ufw allow 80
sudo ufw allow 443
sudo ufw enable
```

## 📊 Monitoring & Logging

### 1. Log Configuration
```python
# settings.py
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': '/var/log/django/legal_assistant.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}
```

### 2. Health Check Endpoint
```python
# views.py
def health_check(request):
    return JsonResponse({'status': 'healthy', 'timestamp': timezone.now()})
```

## 🚀 Performance Optimization

### 1. Database Optimization
```python
# settings.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'legal_assistant',
        'USER': 'django',
        'PASSWORD': 'password',
        'HOST': 'localhost',
        'PORT': '5432',
        'OPTIONS': {
            'MAX_CONNS': 20,
        }
    }
}
```

### 2. Caching
```python
# settings.py
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
    }
}
```

### 3. Static Files CDN
```python
# settings.py
STATIC_URL = 'https://your-cdn-domain.com/static/'
MEDIA_URL = 'https://your-cdn-domain.com/media/'
```

## 🔄 CI/CD Pipeline

### GitHub Actions Example
```yaml
name: Deploy to Production

on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v2
    
    - name: Deploy to Heroku
      uses: akhileshns/heroku-deploy@v3.12.12
      with:
        heroku_api_key: ${{secrets.HEROKU_API_KEY}}
        heroku_app_name: "your-app-name"
        heroku_email: "your-email@example.com"
```

## 📈 Scaling Considerations

### 1. Horizontal Scaling
- Use load balancer (Nginx, HAProxy)
- Multiple application servers
- Database replication
- Redis for session storage

### 2. Vertical Scaling
- Increase server resources
- Optimize database queries
- Use connection pooling
- Implement caching strategies

## 🆘 Troubleshooting

### Common Issues
1. **Static files not loading**: Run `python manage.py collectstatic`
2. **Database connection errors**: Check database credentials and connectivity
3. **Permission errors**: Ensure proper file permissions
4. **Memory issues**: Optimize AI model loading and caching

### Log Locations
- Application logs: `/var/log/django/legal_assistant.log`
- Nginx logs: `/var/log/nginx/error.log`
- System logs: `/var/log/syslog`

---

**Note**: Always test deployment in a staging environment before production deployment.




