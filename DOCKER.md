# Docker Setup for Trax

This guide explains how to run Trax using Docker.

## Prerequisites

- [Docker](https://www.docker.com/products/docker-desktop) installed
- [Docker Compose](https://docs.docker.com/compose/install/) installed

## Quick Start - Development

### 1. Clone the repository
```bash
git clone https://github.com/tatejones2/AssignmentTracker.git
cd AssignmentTracker
```

### 2. Create environment file
```bash
cp .env.example .env
# Edit .env with your settings, especially OPENAI_API_KEY
```

### 3. Build and run with Docker Compose
```bash
docker-compose up --build
```

### 4. Access the application
- **Web App:** http://localhost:8000
- **Database:** localhost:5432

### 5. Create superuser (in a new terminal)
```bash
docker-compose exec web python manage.py createsuperuser
```

### 6. Stop the containers
```bash
docker-compose down
```

---

## Production Deployment

### 1. Set up environment
```bash
cp .env.example .env
# Update .env with production values
# Set DEBUG=False
# Set ALLOWED_HOSTS to your domain
# Set secure database credentials
```

### 2. Build production images
```bash
docker-compose -f docker-compose.prod.yml build
```

### 3. Run production containers
```bash
docker-compose -f docker-compose.prod.yml up -d
```

### 4. Run migrations
```bash
docker-compose -f docker-compose.prod.yml exec web python manage.py migrate
```

### 5. Create superuser
```bash
docker-compose -f docker-compose.prod.yml exec web python manage.py createsuperuser
```

### 6. Collect static files
```bash
docker-compose -f docker-compose.prod.yml exec web python manage.py collectstatic --noinput
```

---

## Useful Docker Commands

### View logs
```bash
# All services
docker-compose logs

# Specific service
docker-compose logs web
docker-compose logs db

# Follow logs in real-time
docker-compose logs -f web
```

### Execute commands in container
```bash
# Run Django management command
docker-compose exec web python manage.py shell

# Create backup
docker-compose exec db pg_dump -U trax_user trax_db > backup.sql

# Restore backup
docker-compose exec -T db psql -U trax_user trax_db < backup.sql
```

### Manage containers
```bash
# Stop containers
docker-compose down

# Remove volumes too (WARNING: deletes data)
docker-compose down -v

# Rebuild images
docker-compose up --build

# View running containers
docker ps

# View all containers
docker ps -a
```

### Database commands
```bash
# Access database shell
docker-compose exec db psql -U trax_user -d trax_db

# Backup database
docker-compose exec db pg_dump -U trax_user trax_db > backup.sql

# Migrate database
docker-compose exec web python manage.py migrate
```

---

## File Descriptions

### `Dockerfile`
- Builds the Django application image
- Installs Python dependencies
- Collects static files
- Sets up Gunicorn as the application server

### `docker-compose.yml` (Development)
- Runs Django development server with hot-reload
- PostgreSQL database with SQLite as fallback
- Mounts local code for live editing
- Exposes ports for debugging

### `docker-compose.prod.yml` (Production)
- Production-ready configuration
- Gunicorn with multiple workers
- Nginx reverse proxy
- Health checks for reliability
- Automatic restarts

### `.env.example`
- Environment variable template
- Copy to `.env` and customize for your setup

### `nginx.conf`
- Production web server configuration
- Static file serving
- Rate limiting
- Security headers
- Gzip compression

---

## Troubleshooting

### Container won't start
```bash
# Check logs
docker-compose logs web

# Check if port 8000 is in use
lsof -i :8000

# Kill process on port 8000
kill -9 $(lsof -t -i:8000)
```

### Database connection refused
```bash
# Wait for database to be ready
docker-compose down
docker-compose up --build

# Check database logs
docker-compose logs db
```

### Static files not showing
```bash
# Collect static files
docker-compose exec web python manage.py collectstatic --noinput

# Check volumes
docker volume ls
```

### Permission denied errors
```bash
# Rebuild without cache
docker-compose build --no-cache

# Reset ownership
docker-compose down -v
docker system prune
docker-compose up --build
```

---

## Deployment to Cloud

### Railway
1. Push to GitHub
2. Connect Railway to your GitHub repo
3. Set environment variables in Railway dashboard
4. Railway automatically detects Dockerfile and deploys

### Render
1. Create Render account
2. Create new Web Service from GitHub
3. Build command: `pip install -r requirements.txt && python manage.py collectstatic --noinput`
4. Start command: `gunicorn config.wsgi:application`
5. Set environment variables

### DigitalOcean App Platform
1. Create DigitalOcean account
2. Create app from GitHub
3. Select Docker runtime
4. Configure environment and deploy

---

## Notes

- Development server auto-reloads on code changes
- Production server uses Gunicorn + Nginx
- All data persists in Docker volumes
- Use `docker-compose down -v` to reset everything

## Support

For issues or questions, check:
- Docker docs: https://docs.docker.com
- Docker Compose docs: https://docs.docker.com/compose
- Django docs: https://docs.djangoproject.com
