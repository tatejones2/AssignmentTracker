# Assignment Tracker

A Django-based web application to track assignments, due dates, and course work.

## Features

- 📝 Create, view, update, and delete assignments
- 📅 Track due dates and course information
- 👤 User authentication and personal assignment management
- 🎯 Django admin panel for easy data management
- ✅ Comprehensive test suite with pytest
- 🔍 Code quality checks with pylint

## Tech Stack

- **Framework:** Django 5.1.2
- **Database:** SQLite (development), PostgreSQL (production-ready)
- **Testing:** pytest, pytest-django, pytest-cov
- **Code Quality:** pylint, pylint-django
- **Python Version:** 3.12+

## Project Structure

```
AssignmentTracker/
├── config/                 # Django project settings
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
├── assignments/           # Main application
│   ├── migrations/
│   ├── tests/            # Test files
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── views.py
│   └── urls.py
├── .venv/                # Virtual environment (not in repo)
├── manage.py             # Django management script
├── requirements.txt      # Python dependencies
├── pytest.ini           # Pytest configuration
├── conftest.py          # Pytest fixtures
├── .pylintrc            # Pylint configuration
├── .gitignore           # Git ignore rules
└── README.md            # This file
```

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/tatejones2/Assignment_Tracker.git
cd Assignment_Tracker
```

### 2. Create Virtual Environment

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run Migrations

```bash
python manage.py migrate
```

### 5. Create Superuser (Admin Account)

```bash
python manage.py createsuperuser
```

### 6. Run Development Server

```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000/` in your browser.

## Testing

### Run All Tests

```bash
pytest
```

### Run Tests with Coverage

```bash
pytest --cov=assignments --cov-report=html
```

View coverage report: `htmlcov/index.html`

### Run Specific Test File

```bash
pytest assignments/tests/test_basic.py
```

## Code Quality

### Run Pylint

```bash
pylint assignments/
```

### Check Specific File

```bash
pylint assignments/models.py
```

## Development Commands

### Create New App

```bash
python manage.py startapp <app_name>
```

### Make Migrations

```bash
python manage.py makemigrations
```

### Apply Migrations

```bash
python manage.py migrate
```

### Access Django Shell

```bash
python manage.py shell
```

### Access Admin Panel

1. Start the server: `python manage.py runserver`
2. Navigate to: `http://127.0.0.1:8000/admin/`
3. Login with superuser credentials

## Environment Variables

Create a `.env` file in the project root for sensitive information:

```env
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

## Contributing

1. Create a new branch: `git checkout -b feature-name`
2. Make your changes
3. Run tests: `pytest`
4. Run linter: `pylint assignments/`
5. Commit changes: `git commit -m "Description"`
6. Push branch: `git push origin feature-name`
7. Create Pull Request

## License

This project is open source and available for educational purposes.

## Author

**Tate Jones** - [tnj@njit.edu](mailto:tnj@njit.edu)

## Repository

[https://github.com/tatejones2/Assignment_Tracker](https://github.com/tatejones2/Assignment_Tracker)
