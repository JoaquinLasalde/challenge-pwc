# Library Management API

A FastAPI application for library management created as part of the PWC challenge.

## Setup

### Prerequisites
- Python 3.10+
- Poetry (dependency management)

### Installation

1. Clone the repository
```bash
git clone <repository-url>
cd <repository-directory>
```

2. Install dependencies with Poetry
```bash
poetry install
```

3. Run the application
```bash
poetry run python run.py
```

The API will be available at `http://localhost:8000`

## API Documentation

Once the application is running, you can access:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Project Structure

The application follows a layered architecture:
- `app/api/routes` - API routes (endpoints)
- `app/services` - Business logic
- `app/models` - Database models
- `app/schemas` - API schemas (Pydantic models)
- `app/db` - Database configuration
- `app/core` - Core application configuration

## Features

- Health and version endpoints
- Library management (Books, Authors, Users, Loans)
- Full CRUD operations for all resources 