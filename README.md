# DRF API

A Django REST Framework API project based on [OpenClassrooms course](https://openclassrooms.com/en/courses/7192416-mettez-en-place-une-api-avec-django-rest-framework).

---

## Table of Contents

- [Quick Start](#quick-start)
- [Setup](#setup)
- [Running the Application](#running-the-application)
- [API Documentation](#api-documentation)
- [Testing](#testing)
- [Code Formatting](#code-formatting)
- [Environment Variables](#environment-variables)
- [Features](#features)
- [Future Improvements](#future-improvements)

---

## Quick Start

### Prerequisites
- Python 3.13+
- pip

### Initial Setup

```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment
# On Linux/Mac:
source .venv/bin/activate
# On Windows:
.venv\Scripts\Activate

# Install dependencies
pip install Django==6.1 djangorestframework drf-spectacular pytest pytest-django

# Apply migrations
python manage.py migrate

# Run the server
python manage.py runserver
```

---

## Setup

The project was initialized with the following commands:

```bash
python -m venv ./.venv
pip install Django==6.1
django-admin startproject training
```

---

## Running the Application

### Start the Development Server

```bash
python manage.py runserver
```

The server runs at `http://127.0.0.1:8000`

### Apply Database Migrations

```bash
python manage.py migrate
```

---

## API Documentation

Once the server is running, access the API documentation at:

- **Swagger UI**: http://127.0.0.1:8000/api/schema/swagger-ui/
- **ReDoc**: http://127.0.0.1:8000/api/schema/redoc/

---

## Testing

### Run All Tests

```bash
pytest
```

### Run a Specific Test

```bash
pytest test_views.py::TestProductViewset::test_filter_products_by_category_id
```

### Test Database

Tests use a temporary test database that's automatically created and rolled back after each test. No mocking is used — real database queries are executed against the test database.

---

## Code Formatting

The project uses **Black** for code formatting.

### Option 1: VS Code Extension (Recommended)

Install the "Black Formatter" extension in VS Code. Code will be formatted automatically on save.

### Option 2: Manual Formatting

```bash
pip install black
black .
```

---

## Environment Variables

The application supports the following environment variables:

| Variable | Purpose | Default |
|----------|---------|---------|
| `DEBUG` | Enable/disable debug mode | `True` |
| `SECRET_KEY` | Django secret key | Insecure dev key |
| `ALLOWED_HOSTS` | Comma-separated allowed hosts | Empty |

### Setup Environment Variables

1. **Copy the example file:**
   ```bash
   cp .env.example .env
   ```

2. **Edit `.env` with your values:**
   ```
   DEBUG=False
   SECRET_KEY=your-secure-secret-key-here
   ALLOWED_HOSTS=localhost,127.0.0.1,example.com
   ```

3. **Load environment variables:**
   
   **Option A: Using python-dotenv (Recommended)**
   ```bash
   pip install python-dotenv
   ```
   Then in your shell before running:
   ```bash
   # Linux/Mac
   export $(cat .env | xargs)
   
   # Windows (PowerShell)
   Get-Content .env | ForEach-Object { $var = $_ -split '='; [Environment]::SetEnvironmentVariable($var[0], $var[1]) }
   ```
   
   **Option B: Export directly in shell**
   ```bash
   export DEBUG=False
   export SECRET_KEY=your-key
   export ALLOWED_HOSTS=localhost,127.0.0.1
   ```

⚠️ **Important:** Never commit `.env` file to version control. Use `.env.example` as a template.

---

## Features

- ✅ Query counting middleware — Tracks database queries per API call in debug logs
- ✅ Category and Product viewsets with full CRUD operations
- ✅ Category disable endpoint — Disables a category and all associated products atomically
- ✅ Product filtering by category
- ✅ Swagger/ReDoc API documentation
- ✅ Comprehensive unit tests with real database

---

## Future Improvements

- [ ] Git pre-commit hook for black formatting and test validation
- [ ] Pagination for list endpoints
- [ ] Authentication and authorization
- [ ] Role-based access control
- [ ] Database connection pooling
- [ ] API rate limiting
