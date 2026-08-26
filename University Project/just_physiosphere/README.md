# Just Physiosphere

A Django-based physiotherapy appointment and management platform with role-based dashboards for patients, therapists, and admins.

## Overview

Just Physiosphere supports:
- Public pages: home, services, about, FAQ, and contact.
- User authentication: registration, login, logout.
- Role-based dashboards:
  - Patient dashboard for booking, rescheduling, and canceling appointments.
  - Therapist dashboard for managing visits, profile, and availability.
  - Admin dashboard for management actions.
- Appointment lifecycle and payment workflow (online and offline simulation flows).
- Medical card and visit records with optional file attachments.
- Basic audit logging and notification hooks.

## Tech Stack

- Python 3.11+
- Django 4.2.10
- SQLite for local development (default)
- MySQL supported for production/staging via environment variables

## Project Structure

```
just_physiosphere/
├── core/                       # Main app: models, views, forms, urls, utils
├── docs/                       # Project docs
├── just_physiosphere/          # Project settings and root urls
├── media/                      # User-uploaded files (ignored in git)
├── static/                     # Source static assets
├── staticfiles/                # Collected static assets (ignored in git)
├── templates/                  # Django templates
├── manage.py
├── requirements.txt
├── .env                        # Local environment variables (ignored in git)
├── .env.example                # Safe environment variable template
└── .gitignore
```

## Environment Variables

The project reads secrets and runtime settings from `.env`.

Create `.env` from `.env.example` and set your own values:

```
DJANGO_SECRET_KEY=unsafe-dev-secret-change-me
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1

DB_ENGINE=django.db.backends.sqlite3
DB_NAME=db.sqlite3

# MySQL example (optional)
# DB_ENGINE=django.db.backends.mysql
# DB_NAME=your_database_name
# DB_USER=your_database_user
# DB_PASSWORD=your_database_password
# DB_HOST=localhost
# DB_PORT=3306

EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
```

Notes:
- Do not use real production credentials in `.env.example`.
- `.env` is ignored by git and should remain local.

## Local Setup

1. Create and activate virtual environment.

Windows (PowerShell):

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

2. Install dependencies.

```powershell
pip install -r requirements.txt
```

3. Configure environment file.

```powershell
Copy-Item .env.example .env
```

4. Local run works as-is with SQLite. If you want MySQL, uncomment the MySQL block in `.env` and set real local values.

5. Apply migrations.

```powershell
python manage.py migrate
```

6. Create admin user.

```powershell
python manage.py createsuperuser
```

7. Run the development server.

```powershell
python manage.py runserver
```

8. Open in browser:
- http://127.0.0.1:8000/
- http://127.0.0.1:8000/admin/

## URL Map (Main Routes)

Public routes:
- /
- /services/
- /about/
- /faq/
- /contact/

Auth routes:
- /login/
- /register/
- /logout/

Dashboard routes:
- /dashboard/
- /dashboard/user/
- /dashboard/therapist/
- /dashboard/admin/

API routes:
- /api/therapist-services/
- /api/available-slots/
- /api/live-serial/

## Security Notes

- Sensitive configuration has been moved to environment variables.
- Keep `DJANGO_DEBUG=False` in production.
- Set `DJANGO_ALLOWED_HOSTS` to production hostnames.
- Rotate keys/passwords immediately if they were ever committed to a remote repository.

## Static and Media

- Source static files live in `static/`.
- Collected static files live in `staticfiles/`.
- Uploaded media lives in `media/`.

For deployment, run:

```powershell
python manage.py collectstatic
```

## Testing

Run tests with:

```powershell
python manage.py test
```

## Git Hygiene

The repository includes `.gitignore` rules for:
- `.env` and secret env variants
- virtual environments
- cache/build artifacts
- collected static and uploaded media

This helps prevent accidental credential or artifact uploads.
