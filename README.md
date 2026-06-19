# School Admin Analytics System

A Django-based school administration analytics system for admins, teachers, and students. The app combines authentication, role-aware navigation, student records, attendance, performance tracking, and Chart.js dashboards into one school performance portal.

## Features

- Role-based access for admins, teachers, and students
- Login, logout, and registration workflows
- Student, course, department, teacher, attendance, and performance models
- Admin analytics dashboard with pass/fail, top students, bottom students, total marks, and department performance charts
- Teacher dashboard with course-level average score, top/bottom students, and low-attendance watchlist
- JSON endpoints for dashboard data consumed by Chart.js
- Responsive sidebar layout and dashboard cards
- MySQL database support with environment-variable configuration
- Regression tests for teacher dashboard routes, data payloads, and access control

## Tech Stack

- Python
- Django 5.2.8
- MySQL / MariaDB
- mysqlclient
- HTML, CSS, JavaScript
- Chart.js

## Database

The default database name is:

```text
student_analyis_db
```

The spelling above matches the existing local MySQL database name used by the project.

Database settings can be overridden with environment variables:

```powershell
$env:DB_NAME='student_analyis_db'
$env:DB_USER='root'
$env:DB_PASSWORD='your_mysql_password'
$env:DB_HOST='127.0.0.1'
$env:DB_PORT='3306'
```

## Local Setup

From the project root:

```powershell
cd "D:\projects\School-admin-analytic-system1-main (2)\School-admin-analytic-system1-main"
```

Activate the existing virtual environment:

```powershell
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, run:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

If `.venv` does not exist, create it:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Run migrations:

```powershell
python manage.py migrate --fake-initial
```

Create an admin user:

```powershell
python manage.py createsuperuser
```

Start the server:

```powershell
python manage.py runserver --insecure
```

Open the app through Django:

```text
http://127.0.0.1:8000/login/
```

Do not open files inside `students/templates/` directly in the browser. Django template files must be rendered through the Django server, otherwise raw template tags like `{% block %}` and `{% url %}` will appear.

## Important Pages

- `/` - Home page
- `/login/` - User login
- `/register/` - User registration
- `/insights/` - Unified analytics page
- `/dashboard-data/` - JSON endpoint for analytics charts
- `/teacher/dashboard/<teacher_id>/` - Teacher dashboard page
- `/teacher/dashboard/data/<teacher_id>/` - Teacher dashboard JSON endpoint
- `/admin/` - Django admin panel

## Quality Assurance

Useful commands:

```powershell
python manage.py check
python manage.py makemigrations --check --dry-run
python manage.py migrate
python manage.py test
python manage.py collectstatic --noinput
```

Current regression coverage includes:

- Teacher dashboard page renders the registered JSON endpoint
- Teacher dashboard returns a safe empty payload when no course is assigned
- Teacher dashboard returns course metrics when data exists
- Teacher dashboard blocks access from other users

## What I Worked On

This project demonstrates full-stack Django development across backend models, authentication, database integration, analytics APIs, and frontend dashboards.

Major work completed:

- Configured the project to use MySQL instead of SQLite
- Connected Django to the local `student_analyis_db` MySQL database
- Fixed migration issues using Django's `--fake-initial` migration flow
- Built role-aware navigation for admin, teacher, and student users
- Implemented analytics endpoints that aggregate attendance and marks data
- Used Chart.js to visualize student and department performance
- Added a teacher dashboard with course analytics and low-attendance tracking
- Fixed frontend rendering issues caused by opening raw Django template files directly
- Improved responsive dashboard styling and layout consistency
- Added regression tests for dashboard access control and JSON data behavior

## Resume Bullets

You can adapt these for your resume:

- Built a role-based school analytics system using Django, MySQL, HTML, CSS, JavaScript, and Chart.js.
- Designed and implemented dashboards for admins and teachers to track student performance, attendance risk, pass/fail trends, and department-level analytics.
- Integrated MySQL with Django ORM models for students, teachers, departments, courses, attendance, and performance records.
- Developed JSON API endpoints for analytics data and connected them to interactive frontend charts.
- Improved application quality by fixing database configuration, migration issues, route bugs, template rendering problems, and dashboard UI defects.
- Added regression tests for teacher dashboard data, route rendering, and user access control.

## LinkedIn Project Summary

I built a School Admin Analytics System using Django, MySQL, and Chart.js to help schools monitor student performance and attendance from one dashboard.

The project includes role-based access for admins, teachers, and students, MySQL-backed data models, analytics JSON endpoints, and interactive charts for pass/fail trends, top and bottom students, total marks, department performance, and teacher-specific course insights.

While building it, I worked through real full-stack problems including database migration issues, role-based routing, template rendering, frontend layout fixes, and regression testing. This project strengthened my skills in Django, MySQL, backend API design, dashboard UI development, and QA.

## How To Explain This Project

Short version:

> I built a Django and MySQL school analytics dashboard that lets admins and teachers monitor student marks, attendance, and performance trends through role-based dashboards and Chart.js visualizations.

Technical version:

> The project uses Django models for students, teachers, departments, courses, attendance, and performance. I created JSON endpoints that aggregate marks and attendance data using Django ORM queries, then rendered the data with Chart.js dashboards. I also configured MySQL, fixed migration conflicts, improved the frontend layout, and added tests for teacher dashboard behavior and access control.

## Future Improvements

- Add more automated tests for registration, login, and admin workflows
- Add CSV import/export for student performance data
- Add teacher course assignment screens in the UI
- Add password reset and email verification
- Improve production deployment settings for HTTPS, secure cookies, and secret management

## GitHub

Repository:

```text
https://github.com/jahidsami985/School-admin-analytic-system1.git
```
