# PMK Consultancy — Enterprise Website Foundation v2

This is a **real, separated Django backend + template/static frontend** with public pages, a database-driven CMS, portfolio, lead intake, role-aware Django Admin, basic audit records, and Docker configuration. It is a **foundation**, not a completed enterprise suite or independently audited security product.

## Layout

- `config/`: Django settings, URLs, WSGI/ASGI
- `website/`: backend models, views, forms, admin, tests, management commands
- `templates/website/`: frontend HTML templates
- `static/css/enterprise.css`: frontend design system and responsive styles
- `static/js/enterprise.js`: navigation interactions
- `media/`: uploaded media (created at runtime)
- `compose.yaml`, `Dockerfile`: deployment scaffolding
- `website/migrations/`: Django schema migrations

## Windows / PowerShell local setup

```powershell
cd D:\PMK\PMK_Consultancy_Enterprise_v2
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Put the generated key in `.env` as `DJANGO_SECRET_KEY=...` (replace the placeholder). Then:

```powershell
python manage.py migrate
python manage.py seed_demo
python manage.py createsuperuser
python manage.py check
python manage.py test
python manage.py runserver
```

Visit `http://127.0.0.1:8000/` and `http://127.0.0.1:8000/secure-admin/`.

## Editable admin modules

- **Site settings**: corporate title, tagline, brand color field, logo, favicon, contact email.
- **Sections**: headings, body copy and image uploads. *Note:* uploaded section backgrounds are stored but not yet applied to all page sections in the templates.
- **Services** and **industries**: create and reorder offerings.
- **Portfolio**: publish genuine work or clearly labeled demo projects.
- **Inquiries**: triage leads, statuses, private internal notes.
- **Audit events**: admin model save/delete operations; not a complete tamper-proof security audit system.
- **Roles**: built-in Django users/groups/permissions. Only trusted staff should have admin access.

## Docker development / production-like staging

Docker is configured for PostgreSQL and Redis but is **not a complete public HTTPS deployment**. Copy `.env.docker.example` to `.env`, change every secret, and set `DJANGO_DEBUG=false`. For initial HTTP localhost staging set `DJANGO_SECURE_SSL_REDIRECT=false` and do not expose it publicly.

```powershell
docker compose up -d --build
docker compose exec web python manage.py migrate
docker compose exec web python manage.py seed_demo
docker compose exec web python manage.py createsuperuser
docker compose exec web python manage.py collectstatic --noinput
docker compose exec web python manage.py check
```

**Important:** production needs a trusted HTTPS reverse proxy, domain, backup and restore testing, security monitoring, static/media delivery design, and secret management. `TRUST_PROXY_SSL_HEADER` should only be enabled behind a correctly configured trusted proxy. HSTS must only be enabled after HTTPS is validated. Do not expose PostgreSQL, Redis or Django Admin without appropriate access controls.

## Security limitations and next priorities

- Django CSRF, session and password validation, ORM query safety, and clickjacking/security headers are configured.
- Inquiry throttling uses Redis in Docker, but is not atomic or sufficient against distributed abuse. Add reverse proxy/WAF throttling and bot mitigation.
- Admin audit events record Django Admin model operations, not logins, API changes or raw SQL; improve immutable centralized auditing.
- Django's image upload validation does not guarantee safe content; use dedicated object storage, strict MIME and size checks, malware scanning, and safe re-encoding before public media hosting.
- Strict CSP is configured; review with all frontend integrations before deploying.
- The app does not currently send email notifications, implement full analytics, expose a public API, support multi-tenant accounts, or contain a drag-and-drop layout editor.
- Change the placeholder contact email and branding; only publish verified case studies.

## Release gate

```powershell
python manage.py test
python manage.py check --deploy
python manage.py collectstatic --noinput
```

`check --deploy` may warn in local debug mode; run it with actual production configuration. Use a staging environment and professional penetration testing before public launch.
