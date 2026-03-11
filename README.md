# Employee Management System

A full-stack Django application with REST API for managing employees via dynamic form templates.

---

## Tech Stack
- **Backend**: Python 3.11, Django 4.2, Django REST Framework
- **Auth**: JWT via `djangorestframework-simplejwt`
- **DB**: PostgreSQL 15
- **Frontend**: Bootstrap 5, Axios (AJAX), SortableJS (drag-and-drop)
- **Container**: Docker + docker-compose

---

## Features
- **Auth**: Register, Login (JWT), Change Password, Profile update
- **Form Builder**: Create dynamic forms with Text, Number, Email, Date, Password, Select, etc. — reorderable via drag-and-drop
- **Employee CRUD**: Create/Edit employees using dynamic form templates — all submissions via Axios (no page reload)
- **Employee Listing**: Search across all field values, filter by form template, delete records
- **REST API**: Full JWT-protected API with Postman collection included

---

## Quick Start (Docker)

### 1. Clone and configure

```bash
git clone https://github.com/akhilpr7/Employee-Management-System.git
cd emp_mgmt
```

### 2. Build and start

```bash
docker-compose up -d --build
```

### 3. Create a superuser (optional)

```bash
docker-compose exec django python manage.py createsuperuser --settings=core.settings.development
```

### 4. Access the app

| URL | Description |
|-----|-------------|
| http://localhost:8000/accounts/login/ | Web login |
| http://localhost:8000/employees/ | Employee list |
| http://localhost:8000/employees/forms/ | Form builder |
| http://localhost:8000/admin/ | Django admin |
| http://localhost:8000/api/ | DRF browsable API |

---

## API Reference

Base URL: `http://localhost/api/`

### Auth Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/auth/register/` | Register new user |
| POST | `/api/auth/login/` | Login → returns JWT tokens |
| POST | `/api/auth/token/refresh/` | Refresh access token |
| GET/PATCH | `/api/auth/profile/` | View/update profile |
| POST | `/api/auth/change-password/` | Change password |
| POST | `/api/auth/logout/` | Blacklist refresh token |

### Form Templates

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/forms/` | List all templates |
| POST | `/api/forms/` | Create template with fields |
| GET | `/api/forms/{id}/` | Get template detail |
| PUT/PATCH | `/api/forms/{id}/` | Update template |
| DELETE | `/api/forms/{id}/` | Delete template |
| GET | `/api/forms/{id}/fields/` | Get fields only |

### Employees

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/employees/` | List (supports ?search=, ?form_template=) |
| POST | `/api/employees/` | Create employee |
| GET | `/api/employees/{id}/` | Get employee detail |
| PATCH | `/api/employees/{id}/` | Update employee |
| DELETE | `/api/employees/{id}/` | Delete employee |

### Authentication Header
```
Authorization: Bearer <access_token>
```

---

## Postman

Import `postman_collection.json` into Postman.  
The collection auto-saves tokens from Login/Register responses into collection variables.

---

## Docker Commands

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f django

# Run migrations
docker-compose exec django python manage.py migrate --settings=core.settings.development

# Shell access
docker-compose exec django python manage.py shell --settings=core.settings.development

# Stop all
docker-compose down

# Stop and remove volumes (full reset)
docker-compose down -v
```

---

