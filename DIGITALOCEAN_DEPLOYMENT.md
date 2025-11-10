# DigitalOcean Deployment Guide for Trax

## Prerequisites
- GitHub account with code pushed
- DigitalOcean account (get $200 free credit for new users!)
- Docker and Docker Compose installed (for local testing)

---

## Option 1: DigitalOcean App Platform (RECOMMENDED - Easiest)

### Why App Platform?
✅ No server management  
✅ Automatic scaling  
✅ Free SSL/HTTPS  
✅ PostgreSQL included  
✅ Deploy with one click  
✅ $5-12/month  

### Step-by-Step Deployment

#### 1. Connect Your GitHub Account
- Go to https://cloud.digitalocean.com/apps
- Click **"Create App"**
- Select **"GitHub"** as the source
- Click **"Authorize DigitalOcean"**
- Select your GitHub account
- Choose **AssignmentTracker** repository
- Select **main** branch

#### 2. Configure App Settings
- DigitalOcean will auto-detect the `app.yaml` file
- Review the configuration - it should show:
  - **Web Service**: Django app with Gunicorn
  - **Database**: PostgreSQL 15
- Click **"Next"**

#### 3. Set Environment Variables
DigitalOcean will prompt you to set these. Add them:

```
DEBUG=False
ENVIRONMENT=production
OPENAI_API_KEY=<your-openai-api-key>
SECRET_KEY=<generate-new-random-key>
ALLOWED_HOSTS=<your-app-name>.ondigitalocean.app
TZ=America/New_York
```

**How to generate SECRET_KEY:**
```bash
python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
```

#### 4. Choose Plan
- **Web Service**: Free or $5/month
- **Database**: Free for 1GB or $15+/month for larger
- Click **"Create Resources"**

#### 5. Wait for Deployment
- This takes 5-10 minutes
- You'll see deployment progress
- Once complete, you'll get a URL: `https://<your-app-name>.ondigitalocean.app`

#### 6. Run Initial Setup
Go to your app console and run:

```bash
# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Collect static files (should be auto)
python manage.py collectstatic --noinput
```

#### 7. Access Your App
- **App URL**: `https://<your-app-name>.ondigitalocean.app`
- **Admin Panel**: `https://<your-app-name>.ondigitalocean.app/admin`

#### 8. Connect Custom Domain (Optional)
- In DigitalOcean console, go to Settings → Domains
- Add your domain
- Update DNS records:
  - Point A record to DigitalOcean's IP
  - Configure CNAME for www (optional)
- Wait for DNS propagation (up to 48 hours)

---

## Option 2: DigitalOcean Droplet + Docker (More Control)

### Why Droplets?
✅ Full server control  
✅ Cheaper if you optimize  
✅ Learn DevOps  
✅ $6/month starting price  

### Step-by-Step Deployment

#### 1. Create a Droplet

**1a. Go to DigitalOcean Console**
- Navigate to https://cloud.digitalocean.com/droplets
- Click **"Create" → "Droplets"**

**1b. Choose Configuration**
- **Image**: Ubuntu 22.04 LTS
- **Size**: $6/month (1GB RAM, 1 vCPU) minimum
- **Region**: Choose closest to your users
- **Authentication**: Add SSH key (recommended) or password
- **Backups**: Optional ($0.80/month)
- Click **"Create Droplet"**

**1c. Note Your IP**
- Copy the Droplet IP address (e.g., `192.168.1.1`)

#### 2. Connect to Your Droplet via SSH

```bash
ssh root@<your-droplet-ip>
```

#### 3. Install Docker & Docker Compose

```bash
# Update system packages
apt update && apt upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh

# Add current user to docker group (optional)
usermod -aG docker ${USER}

# Install Docker Compose
curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose

# Verify installation
docker --version
docker-compose --version
```

#### 4. Clone Your Repository

```bash
# Install Git
apt install -y git

# Clone repository
cd /opt
git clone https://github.com/tatejones2/AssignmentTracker.git
cd AssignmentTracker
```

#### 5. Create Environment File

```bash
# Copy example to .env
cp .env.example .env

# Edit with your settings
nano .env
```

**Required .env values:**
```env
DEBUG=False
SECRET_KEY=<your-generated-key>
ENVIRONMENT=production
OPENAI_API_KEY=<your-key>
ALLOWED_HOSTS=<your-ip-or-domain>
DB_NAME=trax_db
DB_USER=trax_user
DB_PASSWORD=<strong-password>
DB_HOST=db
DB_PORT=5432
TZ=America/New_York
```

Press `Ctrl+X`, then `Y`, then `Enter` to save.

#### 6. Start Docker Containers

```bash
# Build and start services
docker-compose -f docker-compose.prod.yml up -d

# Check status
docker-compose -f docker-compose.prod.yml ps
```

#### 7. Run Initial Setup

```bash
# Run migrations
docker-compose -f docker-compose.prod.yml exec web python manage.py migrate

# Create superuser
docker-compose -f docker-compose.prod.yml exec web python manage.py createsuperuser

# Collect static files
docker-compose -f docker-compose.prod.yml exec web python manage.py collectstatic --noinput
```

#### 8. Configure Firewall

```bash
# Allow SSH, HTTP, HTTPS
ufw allow 22/tcp
ufw allow 80/tcp
ufw allow 443/tcp
ufw enable
```

#### 9. Access Your App
- **Web App**: `http://<your-droplet-ip>:8000`
- After SSL setup: `https://<your-domain>`

#### 10. Connect Custom Domain (Optional)

**Update DNS Records:**
- A record: Points to your Droplet IP
- CNAME (www): Points to your domain

**Set Up HTTPS with Let's Encrypt:**
```bash
# Install Certbot
apt install -y certbot python3-certbot-nginx

# Get certificate
certbot certonly --nginx -d yourdomain.com -d www.yourdomain.com

# Certbot will prompt - follow instructions
# Your cert will be in /etc/letsencrypt/live/yourdomain.com/
```

---

## Managing Your Deployment

### View Logs

**App Platform:**
```bash
# Via DigitalOcean console - click "View Logs"
# Or use doctl CLI:
doctl apps logs <app-id>
```

**Droplet:**
```bash
# View logs
docker-compose -f docker-compose.prod.yml logs -f web

# View database logs
docker-compose -f docker-compose.prod.yml logs -f db

# View nginx logs
docker-compose -f docker-compose.prod.yml logs -f nginx
```

### Update Your Code

**App Platform:**
- Push to GitHub
- DigitalOcean automatically redeploys
- No manual steps needed!

**Droplet:**
```bash
cd /opt/AssignmentTracker

# Pull latest changes
git pull origin main

# Rebuild and restart
docker-compose -f docker-compose.prod.yml up -d --build

# Run any new migrations
docker-compose -f docker-compose.prod.yml exec web python manage.py migrate
```

### Backup Database

**Droplet:**
```bash
# Create backup
docker-compose -f docker-compose.prod.yml exec db pg_dump -U trax_user trax_db > backup.sql

# Restore from backup
docker-compose -f docker-compose.prod.yml exec -T db psql -U trax_user trax_db < backup.sql

# Download backup to local machine
scp root@<droplet-ip>:/opt/AssignmentTracker/backup.sql ~/backup.sql
```

### Stop/Restart Services

**Droplet:**
```bash
# Stop all services
docker-compose -f docker-compose.prod.yml down

# Restart all services
docker-compose -f docker-compose.prod.yml up -d

# Restart specific service
docker-compose -f docker-compose.prod.yml restart web
```

### Monitor Disk Usage

**Droplet:**
```bash
# Check disk space
df -h

# Check Docker images/volumes size
docker system df
```

---

## Troubleshooting

### App won't start

**App Platform:**
1. Go to "Logs" tab
2. Look for error messages
3. Common fixes:
   - Check SECRET_KEY is set
   - Verify OPENAI_API_KEY
   - Check DATABASE_URL format

**Droplet:**
```bash
# Check logs
docker-compose -f docker-compose.prod.yml logs web

# Check if containers are running
docker ps -a

# Restart containers
docker-compose -f docker-compose.prod.yml restart web
```

### Database connection error

**Droplet:**
```bash
# Check database is running
docker ps | grep db

# Check database logs
docker-compose -f docker-compose.prod.yml logs db

# Try to connect directly
docker-compose -f docker-compose.prod.yml exec db psql -U trax_user trax_db
```

### Static files not loading

```bash
# Collect static files again
docker-compose -f docker-compose.prod.yml exec web python manage.py collectstatic --noinput

# Check if files exist
docker-compose -f docker-compose.prod.yml exec web ls -la staticfiles/
```

### Media files not uploading

```bash
# Check media volume permissions
docker-compose -f docker-compose.prod.yml exec web ls -la /app/media/

# Check media directory exists
docker volume ls | grep media
```

---

## Pricing Comparison

| Option | Components | Monthly Cost | Best For |
|--------|------------|--------------|----------|
| **App Platform** | Web ($5) + DB ($15) | **$20+** | Beginners, low maintenance |
| **Droplet** | Droplet ($6) + DB ($15) | **$21+** | Full control, scaling |
| **Free Credit** | All services | **$200 free** | First 2-3 months |

---

## Performance Tips

### App Platform
- Use minimum specs to start
- Scale up if you get traffic
- DigitalOcean handles auto-scaling

### Droplet
- Monitor resource usage: `docker stats`
- Increase workers if CPU high
- Use CDN for static files
- Enable database backups

---

## Security Checklist

✅ Set `DEBUG=False`  
✅ Use strong `SECRET_KEY`  
✅ Never commit `.env` file  
✅ Enable HTTPS/SSL  
✅ Use firewall rules  
✅ Keep Docker images updated  
✅ Regular database backups  
✅ Monitor application logs  

---

## Next Steps After Deployment

1. **Test your app**: Visit your domain and test features
2. **Set up email**: Configure email for notifications
3. **Add monitoring**: Set up uptime monitoring
4. **Schedule backups**: Automate database backups
5. **Performance tune**: Monitor and optimize as needed

---

## Support

- DigitalOcean Docs: https://docs.digitalocean.com
- Docker Docs: https://docs.docker.com
- Django Docs: https://docs.djangoproject.com
- Email support@digitalocean.com for issues

---

## Quick Command Reference

```bash
# Droplet Management
ssh root@<ip>                                    # Connect to droplet
docker-compose -f docker-compose.prod.yml ps    # View containers
docker-compose -f docker-compose.prod.yml logs  # View logs
docker-compose -f docker-compose.prod.yml exec web bash  # Shell access

# Database
docker-compose -f docker-compose.prod.yml exec db psql -U trax_user trax_db  # DB shell
docker-compose -f docker-compose.prod.yml exec web python manage.py shell   # Django shell

# Updates
git pull origin main                             # Get latest code
docker-compose -f docker-compose.prod.yml up -d --build  # Rebuild & restart
docker-compose -f docker-compose.prod.yml exec web python manage.py migrate  # Run migrations
```

---

**You're all set! Your Trax app is ready to deploy to DigitalOcean!** 🚀
