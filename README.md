# School Admin Analytic System

A Django-based school administration dashboard that provides student, teacher, and admin analytics in one unified insights page.

## Features

- Authentication and role-based access for admins, teachers, and students
- Unified analytics page with interactive charts
- Dashboard data served as JSON for Chart.js visualizations
- Responsive layout and polished insights card styling

## Key Pages

- `/` - Home and login/register entry point
- `/insights/` - Unified analytics page for all authenticated users
- `/dashboard-data/` - JSON endpoint for dashboard chart data

## Installation

1. Clone the repository
2. Create a Python virtual environment
3. Install dependencies
4. Configure `school_admin_panel/settings.py` for your database
5. Run migrations
6. Create a superuser

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## Dependencies

This project depends on the following Python packages:

- `Django==5.2.8`
- `mysqlclient==2.2.8`
- `asgiref==3.11.1`
- `sqlparse==0.5.5`
- `tzdata==2026.2`

## Notes

- This repo was initialized locally and the current commit includes improved analytics styling and a stable chart layout.
- The analytics page uses Chart.js for charts and sets fixed canvas heights to prevent layout drift.

## GitHub

Pushed to `https://github.com/jahidsami985/School-admin-analytic-system1.git` on branch `master`.
