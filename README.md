# Django Project Deployment Guide
> A comprehensive guide for deploying Django applications using Vercel (server) and Neon.tech (database)

## Table of Contents
- [Database Setup with Neon.tech](#database-setup-with-neontech)
- [Project Deployment with Vercel](#project-deployment-with-vercel)
- [Configuration Files](#configuration-files)
- [Troubleshooting](#troubleshooting)

## Database Setup with Neon.tech

### Step 1: Create Neon.tech Account
1. Visit [neon.tech](https://neon.tech)
2. Sign up for a new account
3. Verify your email address

### Step 2: Database Configuration
1. Create a New Project
2. Navigate to QuickStart > postgres
3. Wait for the connection string generation
4. Copy the generated database connection string

### Step 3: Django Database Configuration
1. Install required dependencies:
```bash
pip install psycopg2-binary dj-database-url
pip freeze > requirements.txt
```

`IMPORTANT:` Please clean up the `requirements.txt` file by removing unnecessary packages. It should only include the essential libraries/packages. Below is a sample file for reference:

`requirements.txt:`

```
dj-database-url==2.3.0
Django==5.1.3
djangorestframework==3.15.2
gunicorn==23.0.0
psycopg2-binary==2.9.10
python-dateutil
python-decouple==3.8
requests==2.32.3
whitenoise==6.8.2
```

2. Update your `settings.py`:
```python
import dj_database_url

DATABASES = {
    'default': dj_database_url.parse(
        "your-generated-database-connection-string"
    )
}
```

3. Run migrations:
```bash
python manage.py migrate
```

## Project Deployment with Vercel

### Step 1: Initial Setup
1. Visit [Vercel's Django Template](https://vercel.com/templates/python/django-hello-world)
2. Click "Deploy" and connect with your GitHub account
3. Clone the newly created repository:
```bash
git clone <your-repo-url>
```

### Step 2: Update Repository with Existing Project
1. Copy your existing Django project files into the cloned directory
2. Ensure to maintain the following structure:
   ```
   your-project/
   ├── your_project_name/
   │   ├── __init__.py
   │   ├── settings.py
   │   ├── urls.py
   │   └── wsgi.py
   ├── manage.py
   ├── requirements.txt
   ├── vercel.json
   └── vercel.sh
   ```
3. Update all file paths in configuration files to match your project name
4. Commit and push your changes:
   ```bash
   git add .
   git commit -m "Update with existing project"
   git push origin main
   ```

### Step 3: Project Configuration
Create or update the following configuration files in your project:

1. `vercel.json`:
```json
{
  "version": 2,
  "builds": [
    {
      "src": "your_project_name/wsgi.py",
      "use": "@vercel/python",
      "config": {
        "maxLambdaSize": "15mb",
        "runtime": "python3.12"
      }
    },
    {
      "src": "vercel.sh",
      "use": "@vercel/static-build",
      "config": {
        "distDir": "assets/staticfiles"
      }
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "your_project_name/wsgi.py"
    }
  ],
  "env": {
    "PYTHONPATH": "./",
    "DJANGO_SETTINGS_MODULE": "your_project_name.settings",
    "SITE_DOMAIN": "your-vercel-deployment-url"
  }
}
```

2. `vercel.sh`:
```bash
#!/bin/bash
echo -e "Installing dependencies"
python3.12 -m pip install -r requirements.txt

echo -e "Applying migrations..."
python3.12 manage.py migrate

echo -e "Running custom initialization command..."
python3.12 manage.py init

echo -e "Collecting static files..."
python3.12 manage.py collectstatic --noinput

echo -e "Deployment script completed."
```

3. Update `settings.py`:
```python
DEBUG = False

ALLOWED_HOSTS = [".vercel.app"]

MIDDLEWARE = [
    # ... existing middleware ...
    "whitenoise.middleware.WhiteNoiseMiddleware",
]

STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'assets', 'staticfiles')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'your_app_name', 'static'),
]

WSGI_APPLICATION = 'your-project-name.wsgi.app'
```

4. Update `wsgi.py`:
```python
import os
from django.core.wsgi import get_wsgi_application
from whitenoise import WhiteNoise

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'your_project_name.settings')
static_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "assets", "staticfiles"))

app = get_wsgi_application()
app = WhiteNoise(app, root=static_root)
```

5. Create/update `requirements.txt` with only necessary packages.

### Step 3: Deployment
1. Commit all changes to your repository:
```bash
git add .
git commit -m "Deployment configuration"
git push
```

2. Vercel will automatically detect the changes and deploy your application.

## Troubleshooting
- If static files are not loading, ensure your `STATIC_ROOT` and `STATICFILES_DIRS` paths are correct
- For database connection issues, verify your Neon.tech connection string
- Check Vercel deployment logs for specific error messages

## Support
For additional help:
- [Vercel Documentation](https://vercel.com/docs)
- [Neon.tech Documentation](https://neon.tech/docs)
- [Django Documentation](https://docs.djangoproject.com/)