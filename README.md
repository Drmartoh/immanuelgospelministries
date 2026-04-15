# Immanuel Gospel Ministries Web App

Production-ready Django church management and public website built with Python, Tailwind CSS, and JavaScript (Alpine.js + AOS).

## Features

- Dynamic homepage, about, services, events, sermons, prayer requests, giving, and contact pages.
- Admin-manageable content for church info, history, core values, events, sermons, prayer requests, messages, and members.
- Responsive modern UI with sticky nav, cards, scroll animations, and floating WhatsApp button.
- SQLite database and PythonAnywhere-ready static/media configuration.

## Setup

1. Create and activate a virtual environment.
2. Install dependencies:
   - `pip install -r requirements.txt`
3. Run migrations:
   - `python manage.py makemigrations`
   - `python manage.py migrate`
4. Seed initial content:
   - `python manage.py seed_data`
5. Create admin user:
   - `python manage.py createsuperuser`
6. Run development server:
   - `python manage.py runserver`

## Admin Login

- URL: `/admin/`
- Use the superuser credentials created with `createsuperuser`.

## PythonAnywhere Notes

- Set environment variables:
  - `DJANGO_DEBUG=False`
  - `DJANGO_SECRET_KEY=<your-secret-key>`
- Ensure static files are collected:
  - `python manage.py collectstatic --noinput`
- Configure:
  - Static URL: `/static/` mapped to `staticfiles`
  - Media URL: `/media/` mapped to `media`
- WSGI entry point: `immanuel_project.wsgi:application`
