# Hirewell — Django Implementation

Server-rendered version of the job portal, built with Django, Django ORM and Django REST Framework (used for the read-only `/api/` endpoints).

## Stack

Python 3.11+, Django 5, Django REST Framework, django-filter, SQLite (default) or PostgreSQL, WhiteNoise for static files, Pillow for image fields.

## Setup

```bash
cd django-version
python -m venv venv
source venv/bin/activate        # venv\Scripts\activate on Windows
pip install -r requirements.txt

cp .env.example .env             # then fill in DJANGO_SECRET_KEY
python manage.py migrate
python manage.py seed_data       # optional: wipes DB and loads fictional demo data
python manage.py createsuperuser # optional: if you don't want to use the seeded admin
python manage.py runserver
```

Visit `http://127.0.0.1:8000`.

## Environment variables (`.env`)

| Variable | Purpose |
|---|---|
| `DJANGO_SECRET_KEY` | Required. Generate with `python -c "import secrets; print(secrets.token_urlsafe(50))"` |
| `DJANGO_DEBUG` | `True` for local dev, `False` in production |
| `DJANGO_ALLOWED_HOSTS` | Comma-separated hostnames |

## Database

Defaults to SQLite (`db.sqlite3`) for zero-config local development. To use PostgreSQL, install `psycopg2-binary`, add it to `requirements.txt`, and change `DATABASES` in `config/settings.py` to point at your Postgres instance.

## Demo accounts (after `seed_data`)

All demo accounts share the password `Password123!`.

| Role | Email |
|---|---|
| Admin (Django admin + platform dashboard) | `admin@demo.test` |
| Candidate | `seeker@demo.test` / `priya@demo.test` |
| Employer | `employer@demo.test` / `mei@demo.test` |

Django's built-in admin is available at `/admin/`.

## App layout

- `accounts/` — custom `User` model (email-based login), registration/login/logout, candidate profile, resume upload/download
- `companies/` — employer company profile
- `jobs/` — job model, public search/filter/detail, saved jobs, categories
- `applications/` — application model, cover letters, status history, interviews, applicant management
- `notifications/` — lightweight in-app notification model + context processor
- `dashboard/` — employer and admin dashboards (stats, job & user management)
- `config/` — settings, root URLs, and the DRF router for `/api/`

## REST API

Read-mostly DRF endpoints live under `/api/`: `/api/jobs/`, `/api/categories/`, `/api/companies/`, `/api/applications/` (scoped to the authenticated user's role). These use Django's session authentication, so they're intended for the same-origin server-rendered app, not a separate SPA.

## Testing performed

Verified with Django's test client: home/list/detail pages, registration, login (email as username), profile editing, resume upload with a resume-required gate on applying, duplicate-application prevention, employer job creation with server-side salary/deadline validation, applicant status updates, and role-gated dashboards (403 on cross-role access, 404/500 custom pages).

## Known limitations

- Email sending uses Django's console backend (prints to stdout) — swap `EMAIL_BACKEND` for SMTP/SES in production.
- File uploads are stored on local disk (`media/`); swap `DEFAULT_FILE_STORAGE` for S3-compatible storage in production.
- No automated test suite (`tests.py` files) is included yet — see the root README's "Future improvements".
