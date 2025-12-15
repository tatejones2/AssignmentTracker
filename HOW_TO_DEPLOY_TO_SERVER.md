# Django AssignmentTracker Deployment Guide

**Project:** AssignmentTracker (Django Web App)  
**Server:** Digital Ocean Droplet  
**Domain:** taterdoesschool.com  
**Server IP:** 64.225.24.213  
**Infrastructure Path:** `~/mywebclass_hosting/infrastructure`

## Table of Contents

1. [Overview](#overview)
2. [Prerequisites](#prerequisites)
3. [Directory Structure](#directory-structure)
4. [Django Application Setup](#django-application-setup)
5. [Docker Configuration](#docker-configuration)
6. [Caddy Configuration](#caddy-configuration)
7. [Docker Compose Setup](#docker-compose-setup)
8. [Deployment Steps](#deployment-steps)
9. [SSL/HTTPS Configuration](#sslhttps-configuration)
10. [Troubleshooting](#troubleshooting)

---

## Overview

This guide walks through deploying a Django application (AssignmentTracker) on a Digital Ocean droplet using:
- **Caddy** as the reverse proxy and HTTPS terminator
- **Docker** for containerization
- **Docker Compose** for orchestration

The setup runs from `~/mywebclass_hosting/infrastructure` where the Caddyfile is located.

---

## Prerequisites

Before deployment, ensure:

- SSH access to the server (64.225.24.213)
- Domain configured to point to server IP (taterdoesschool.com)
- Docker and Docker Compose installed on the droplet
- Git installed for repository cloning
- Python 3.8+ for local development/testing

**Install dependencies on droplet:**

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Install Caddy
sudo apt install -y caddy
```

---

## Directory Structure

On the droplet, organize the project as:

```
~/mywebclass_hosting/
├── infrastructure/
│   ├── Caddyfile                    # Caddy reverse proxy config
│   ├── docker-compose.yml           # Docker Compose orchestration
│   ├── docker-compose.prod.yml      # Production overrides (optional)
│   └── .env                         # Environment variables (NEVER commit)
│
└── assignmenttracker/               # Django project repository
    ├── Dockerfile                   # Django app container
    ├── requirements.txt             # Python dependencies
    ├── manage.py
    ├── assignmenttracker/           # Django project folder
    │   ├── settings.py
    │   ├── urls.py
    │   ├── wsgi.py
    │   └── asgi.py
    ├── app/                         # Django apps
    └── static/                      # Static files
```

---

## Django Application Setup

### 1. Create Django Project Structure

```bash
cd ~/mywebclass_hosting
git clone <your-assignmenttracker-repo> assignmenttracker
cd assignmenttracker
```

### 2. Create requirements.txt

Ensure your `requirements.txt` includes:

```
Django==4.2.0
djangorestframework==3.14.0
python-dotenv==1.0.0
gunicorn==21.2.0
psycopg2-binary==2.9.0
redis==5.0.0
```

### 3. Configure Django Settings

In `assignmenttracker/settings.py`:

```python
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# Security Settings
DEBUG = os.getenv('DEBUG', 'False') == 'True'
ALLOWED_HOSTS = ['taterdoesschool.com', '64.225.24.213', 'localhost']
SECRET_KEY = os.getenv('SECRET_KEY', 'change-me-in-production')

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME', 'assignmenttracker'),
        'USER': os.getenv('DB_USER', 'postgres'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST', 'db'),
        'PORT': os.getenv('DB_PORT', '5432'),
    }
}

# Static Files
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Redis Cache
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://cache:6379/1',
    }
}
```

---

## Docker Configuration

### Dockerfile

Create `Dockerfile` in the AssignmentTracker root:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

# Collect static files
RUN python manage.py collectstatic --noinput

# Run Gunicorn
CMD ["gunicorn", "assignmenttracker.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "4"]
```

### .dockerignore

```
.git
.gitignore
.env
.venv
venv/
__pycache__
*.pyc
db.sqlite3
.pytest_cache
.coverage
htmlcov/
.DS_Store
```

---

## Caddy Configuration

Edit the Caddyfile at `~/mywebclass_hosting/infrastructure/Caddyfile`:

```caddy
taterdoesschool.com {
    # Proxy to Django app running in Docker
    reverse_proxy assignmenttracker:8000 {
        # Add headers for Django
        header_up X-Forwarded-For {http.request.remote}
        header_up X-Forwarded-Proto {http.request.proto}
        header_up X-Forwarded-Host {http.request.host}
    }
    
    # Serve static files (optional if using WhiteNoise)
    # handle /static/* {
    #     root * /var/www/static
    #     file_server
    # }
    
    # Enable HTTPS (automatic via Let's Encrypt)
    encode gzip
}

# Redirect www to non-www
www.taterdoesschool.com {
    redir https://taterdoesschool.com{uri}
}
```

---

## Docker Compose Setup

Create `docker-compose.yml` in `~/mywebclass_hosting/infrastructure/`:

```yaml
version: '3.8'

services:
  db:
    image: postgres:15
    container_name: assignmenttracker_db
    environment:
      POSTGRES_DB: ${DB_NAME:-assignmenttracker}
      POSTGRES_USER: ${DB_USER:-postgres}
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    networks:
      - assignmenttracker_network
    restart: unless-stopped

  cache:
    image: redis:7-alpine
    container_name: assignmenttracker_cache
    networks:
      - assignmenttracker_network
    restart: unless-stopped

  assignmenttracker:
    build: ../assignmenttracker
    container_name: assignmenttracker
    depends_on:
      - db
      - cache
    environment:
      DEBUG: ${DEBUG:-False}
      SECRET_KEY: ${SECRET_KEY}
      DB_NAME: ${DB_NAME:-assignmenttracker}
      DB_USER: ${DB_USER:-postgres}
      DB_PASSWORD: ${DB_PASSWORD}
      DB_HOST: db
      DB_PORT: 5432
      REDIS_HOST: cache
      REDIS_PORT: 6379
    volumes:
      - ../assignmenttracker/static:/app/staticfiles
    networks:
      - assignmenttracker_network
    restart: unless-stopped

  caddy:
    image: caddy:2-alpine
    container_name: assignmenttracker_caddy
    depends_on:
      - assignmenttracker
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./Caddyfile:/etc/caddy/Caddyfile
      - caddy_data:/data
      - caddy_config:/config
    networks:
      - assignmenttracker_network
    restart: unless-stopped

volumes:
  postgres_data:
  caddy_data:
  caddy_config:

networks:
  assignmenttracker_network:
    driver: bridge
```

### Environment File

Create `.env` in `~/mywebclass_hosting/infrastructure/`:

```bash
# Django
DEBUG=False
SECRET_KEY=your-super-secret-key-change-this
ALLOWED_HOSTS=taterdoesschool.com,64.225.24.213

# Database
DB_NAME=assignmenttracker
DB_USER=postgres
DB_PASSWORD=your-secure-database-password

# Redis
REDIS_HOST=cache
REDIS_PORT=6379
```

**Security Note:** Never commit `.env` to version control. Add to `.gitignore`:

```
.env
.env.local
*.key
```

---

## Deployment Steps

### 1. Connect to Droplet

```bash
ssh root@64.225.24.213
```

### 2. Clone/Update Repository

```bash
cd ~/mywebclass_hosting
git clone <repo-url> assignmenttracker
# OR update existing: cd assignmenttracker && git pull
```

### 3. Set Up Environment Variables

```bash
cd ~/mywebclass_hosting/infrastructure
nano .env
# Add all required environment variables
```

### 4. Build and Start Containers

```bash
cd ~/mywebclass_hosting/infrastructure
docker-compose build
docker-compose up -d
```

### 5. Run Django Migrations

```bash
docker-compose exec assignmenttracker python manage.py migrate
```

### 6. Create Superuser (First Time Only)

```bash
docker-compose exec assignmenttracker python manage.py createsuperuser
```

### 7. Collect Static Files

```bash
docker-compose exec assignmenttracker python manage.py collectstatic --noinput
```

### 8. Verify Deployment

```bash
# Check running containers
docker-compose ps

# View logs
docker-compose logs -f caddy
docker-compose logs -f assignmenttracker

# Test domain
curl https://taterdoesschool.com
```

---

## SSL/HTTPS Configuration

Caddy automatically handles SSL/TLS with Let's Encrypt:

- **Automatic renewal:** Certificates auto-renew before expiration
- **No manual configuration needed** if DNS is pointing to server IP
- **Verification:** `curl -I https://taterdoesschool.com` should return 200

If SSL fails:
1. Verify DNS points to 64.225.24.213
2. Ensure ports 80 and 443 are open in firewall
3. Check Caddy logs: `docker-compose logs caddy`

---

## Troubleshooting

### Container won't start

```bash
# View detailed logs
docker-compose logs assignmenttracker

# Check if port 8000 is already in use
docker ps | grep 8000

# Rebuild without cache
docker-compose build --no-cache
```

### Database connection error

```bash
# Check PostgreSQL container
docker-compose logs db

# Verify environment variables
docker-compose config | grep DB_

# Manually test connection
docker-compose exec db psql -U postgres -c "SELECT 1"
```

### Static files not loading

```bash
# Collect static files
docker-compose exec assignmenttracker python manage.py collectstatic --noinput

# Verify volume mount
docker inspect assignmenttracker | grep -A 5 Mounts
```

### Domain not resolving

```bash
# Test DNS
nslookup taterdoesschool.com

# Verify Caddy is running
docker-compose ps caddy

# Check Caddy config syntax
docker-compose exec caddy caddy validate --config /etc/caddy/Caddyfile
```

### Restart All Services

```bash
cd ~/mywebclass_hosting/infrastructure
docker-compose down
docker-compose up -d
```

### View Real-Time Logs

```bash
docker-compose logs -f assignmenttracker
docker-compose logs -f caddy
docker-compose logs -f db
```

---

## Production Checklist

- [ ] Change all default passwords
- [ ] Set `DEBUG=False` in `.env`
- [ ] Generate strong `SECRET_KEY`
- [ ] Configure `ALLOWED_HOSTS` correctly
- [ ] Set up database backups
- [ ] Enable Django security middleware
- [ ] Configure CORS if needed
- [ ] Set up log aggregation
- [ ] Configure error monitoring (Sentry)
- [ ] Document deployment process
- [ ] Set up automated backups

---

## Next Steps

1. Deploy AssignmentTracker
2. Test all functionality
3. Monitor logs for errors
4. Set up automated backups
5. Configure monitoring/alerting

For issues or updates, refer to:
- [Django Documentation](https://docs.djangoproject.com/)
- [Docker Compose Docs](https://docs.docker.com/compose/)
- [Caddy Docs](https://caddyserver.com/docs/)
