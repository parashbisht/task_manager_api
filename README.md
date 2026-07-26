# Task Manager API

A production-style REST API for managing tasks, built with FastAPI and PostgreSQL. Each user authenticates via JWT and only sees their own tasks.

## Features

- JWT authentication (signup, login, protected routes)
- Full task CRUD, scoped per user
- Mark tasks complete
- Input validation and proper HTTP status codes (401, 404, 409, 422)
- Database migrations with Alembic
- Automated tests with Pytest
- Dockerized, with CI running tests on every push

## Tech Stack

FastAPI, PostgreSQL, SQLAlchemy 2.0, Alembic, JWT (python-jose), Passlib (bcrypt), Pytest, Docker, GitHub Actions

## API Endpoints

| Method | Endpoint | Description | Auth |
|---|---|---|---|
| GET | /  | Welcome message | No |
| GET | /health | Health check | No |
| POST | /auth/signup | Create an account | No |
| POST | /auth/login | Log in, returns a JWT | No |
| GET | /auth/me | Current user info | Yes |
| GET | /tasks | List your tasks | Yes |
| GET | /tasks/{id} | Get a task | Yes |
| POST | /tasks | Create a task | Yes |
| PUT | /tasks/{id} | Update a task | Yes |
| PATCH | /tasks/{id}/complete | Mark complete | Yes |
| DELETE | /tasks/{id} | Delete a task | Yes |

## Quick Start (Docker)

    git clone https://github.com/parashbisht/task_manager_api.git
    cd task_manager_api
    cp .env.example .env
    docker compose up --build

API runs at http://127.0.0.1:8000/docs

## Running Locally (without Docker)

    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    sudo service postgresql start
    sudo -u postgres psql -c "CREATE DATABASE task_manager;"
    cp .env.example .env
    python3 -c "import secrets; print(secrets.token_hex(32))"
    alembic upgrade head
    uvicorn app.main:app --reload

## Running Tests

    pytest -v

Tests run against a separate task_manager_test database. CI runs the same suite automatically on every push via GitHub Actions.

## Project Structure

    app/
    main.py       - routes
    config.py     - settings from .env
    database.py   - SQLAlchemy engine/session
    models.py     - User and Task ORM models
    schemas.py    - Pydantic schemas
    crud.py       - database operations
    security.py   - password hashing, JWT
    deps.py       - auth dependency

    alembic/           - migrations
    tests/             - pytest suite
    .github/workflows/ - CI pipeline
