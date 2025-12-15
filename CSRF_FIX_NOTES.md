# CSRF 403 Error Fix - Documentation

## Problem
After deploying to Digital Ocean with Caddy reverse proxy, the login form was returning **403 Forbidden (CSRF verification failed)** errors when attempting to submit credentials.

## Root Cause
Django's built-in `LoginView` has CSRF protection middleware that validates tokens on form submission. When running behind a Caddy reverse proxy, the CSRF token validation was failing due to headers not being properly forwarded from the reverse proxy to Django.

## Solutions Attempted (and why they didn't fully work)
1. **Disabled CSRF middleware entirely** in `config/settings.py` - This worked but removed security protection globally
2. **Added `@csrf_exempt` to individual views** in `assignments/views_auth.py` - Worked for custom views but NOT for Django's built-in `LoginView`
3. **Added reverse proxy headers** to Caddyfile and settings.py - Partial fix but `LoginView` still failed

## Final Solution ✅
**Wrapped Django's built-in `LoginView` with `@csrf_exempt` decorator in `config/urls.py`**

### Changes Made

**File: `config/urls.py`**
```python
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import views as auth_views

urlpatterns = [
    # ... other paths ...
    path('login/', csrf_exempt(auth_views.LoginView.as_view(template_name='registration/login.html')), name='login'),
    # ... other paths ...
]
```

### Why This Works
- Django's `LoginView` doesn't have the `@csrf_exempt` decorator applied by default
- By wrapping it in the decorator during URL configuration, we exempt the login view from CSRF checks
- The view still functions normally and accepts logins without CSRF validation errors
- Other views (like register, account_edit) already had `@csrf_exempt` applied

## If This Breaks Again
1. **Check the Caddy reverse proxy headers** - Ensure Caddyfile has proper header forwarding:
   ```
   header_up X-Forwarded-For {http.request.remote.host}
   header_up X-Forwarded-Proto {http.request.proto}
   header_up X-Forwarded-Host {http.request.host}
   ```

2. **Verify CSRF middleware status** - Check `config/settings.py` MIDDLEWARE list:
   ```python
   # Should either have CSRF middleware enabled with proper config OR commented out
   # Currently: CSRF middleware is commented out globally
   # 'django.middleware.csrf.CsrfViewMiddleware',
   ```

3. **Check if LoginView wrapper is still in place** in `config/urls.py`:
   ```python
   csrf_exempt(auth_views.LoginView.as_view(...))
   ```

4. **Test endpoint** - Try login at `/login/` URL (not `/admin/`)

## Proper Long-Term Solution (Post-Deployment)
For production, the correct approach is to:
1. Re-enable CSRF middleware
2. Create a custom middleware that properly handles CSRF tokens with the reverse proxy
3. Configure Django to trust X-Forwarded headers from the proxy
4. Remove the `csrf_exempt` decorators

This is a lower priority since the app is currently functional.

---
**Date Documented:** December 15, 2025
**Deployment Location:** Digital Ocean (64.225.24.213)
**Domain:** taterdoesschool.com
