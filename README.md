# College Attendance Management System
Django + SQLite mini project.

Roles: Admin, Faculty, Student
Years: 1st, 2nd, 3rd
Statuses: Present, Absent, OD, ML

Setup:
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
