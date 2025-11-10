# DigitalOcean Deployment Checklist

Use this checklist to ensure your Trax app is ready for DigitalOcean deployment.

## Pre-Deployment (Local Testing)

- [ ] Run `docker-compose up --build` locally
- [ ] Test all features work in Docker
- [ ] Run migrations: `docker-compose exec web python manage.py migrate`
- [ ] Create superuser: `docker-compose exec web python manage.py createsuperuser`
- [ ] Access http://localhost:8000 and verify app works
- [ ] Test login with superuser
- [ ] Create test assignment and check features
- [ ] Push all code to GitHub: `git push origin main`

## Environment Setup

- [ ] Copy `.env.example` to `.env`
- [ ] Generate secure `SECRET_KEY`:
  ```bash
  python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
  ```
- [ ] Add `OPENAI_API_KEY` (get from https://platform.openai.com)
- [ ] Set `DEBUG=False`
- [ ] Set `ENVIRONMENT=production`
- [ ] Set `ALLOWED_HOSTS` (will update after deployment)
- [ ] Set strong database password: `DB_PASSWORD`
- [ ] Never commit `.env` file

## DigitalOcean Configuration

### Database
- [ ] Choose PostgreSQL 15 (recommended)
- [ ] Set strong `DB_PASSWORD`
- [ ] Note database credentials

### Environment Variables
Set these in DigitalOcean dashboard:
- [ ] `DEBUG=False`
- [ ] `SECRET_KEY=<generated-key>`
- [ ] `ENVIRONMENT=production`
- [ ] `OPENAI_API_KEY=<your-key>`
- [ ] `ALLOWED_HOSTS=<your-domain>`
- [ ] `TZ=America/New_York`

### App Platform Configuration
- [ ] App name set (e.g., "trax")
- [ ] Build command verified
- [ ] Run command verified
- [ ] Health check path: `/health/`
- [ ] Port: 8080

## Post-Deployment

- [ ] App is accessible at assigned URL
- [ ] Admin panel works: `/admin`
- [ ] Can log in with superuser
- [ ] Can create assignments
- [ ] Static files load (CSS/JS visible)
- [ ] Media files work (podcast uploads)
- [ ] Database migrations applied

## Security

- [ ] DEBUG set to False
- [ ] SECRET_KEY is unique and strong
- [ ] ALLOWED_HOSTS configured
- [ ] HTTPS/SSL enabled
- [ ] Database password is strong
- [ ] `.env` not in version control

## Optional Enhancements

- [ ] Custom domain configured
- [ ] Email notifications set up
- [ ] Database backups configured
- [ ] Monitoring/alerts set up
- [ ] CDN for static files
- [ ] Rate limiting configured

## Monitoring

- [ ] Check app logs regularly
- [ ] Monitor database size
- [ ] Track resource usage
- [ ] Set up error notifications
- [ ] Test health check endpoint: `/health/`

## First Time Updates

After deployment, if you make changes:

**App Platform (automatic):**
1. Push to GitHub
2. DigitalOcean automatically redeploys

**Droplet (manual):**
```bash
ssh root@<ip>
cd /opt/AssignmentTracker
git pull origin main
docker-compose -f docker-compose.prod.yml up -d --build
docker-compose -f docker-compose.prod.yml exec web python manage.py migrate
```

## Troubleshooting Checklist

- [ ] Check app logs for errors
- [ ] Verify all environment variables are set
- [ ] Confirm database connection works
- [ ] Test health check: `curl https://<your-domain>/health/`
- [ ] Check if static files are served
- [ ] Verify media files upload directory permissions
- [ ] Ensure migrations are applied

## Backup Strategy

- [ ] Enable daily database backups
- [ ] Download backup weekly: `docker-compose exec db pg_dump -U trax_user trax_db > backup.sql`
- [ ] Store backups in safe location
- [ ] Test restore process

## Performance

- [ ] Monitor CPU usage
- [ ] Monitor memory usage
- [ ] Check response times
- [ ] Review error rates
- [ ] Optimize database queries if needed

---

## Getting Help

If deployment fails:

1. Check logs: View in DigitalOcean console or `docker-compose logs`
2. Verify environment variables are all set
3. Run `docker-compose exec web python manage.py check`
4. Read error messages carefully
5. Check:
   - Django docs: https://docs.djangoproject.com
   - DigitalOcean docs: https://docs.digitalocean.com
   - Docker docs: https://docs.docker.com

---

## Success! 🎉

Once all items are checked:
- [ ] Your Trax app is live on DigitalOcean
- [ ] Users can access it at your domain
- [ ] Data is persisted and backed up
- [ ] Monitoring is in place
- [ ] You're ready for production use!

**Date deployed:** ___________  
**Deployment URL:** ___________  
**Notes:** ___________
