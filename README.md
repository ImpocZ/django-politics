# Django backend for Politicians

This repository contains a minimal Django backend and a `politicians` app.

Quick setup:

1. Create and activate a virtual environment

```powershell
python -m venv env
env\Scripts\Activate.ps1
```

2. Install dependencies

```powershell
pip install -r requirements.txt
```

3. Apply migrations and create an admin user

```powershell
python manage.py migrate
python manage.py createsuperuser
```

4. Run the development server

```powershell
python manage.py runserver
```

Admin site will be available at `http://127.0.0.1:8000/admin/`.

