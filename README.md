# Library Management API

A FastAPI application for library management that follows a layered architecture pattern.

## Features

- Full CRUD operations for authors, books, users, and loans
- Business logic transformations such as book availability and author statistics
- Proper error handling and validation
- Documented database schema and integration patterns
- Swagger documentation

## Prerequisites

- Python 3.8+
- pip

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/library-management-api.git
cd library-management-api
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Application

To run the application in development mode:

```bash
uvicorn app.main:app --reload --port 8001
```

The API will be available at `http://localhost:8001`.

- API documentation: `http://localhost:8001/docs`
- Alternative documentation: `http://localhost:8001/redoc`

## Running with Docker

### Using Docker Compose (Recommended)

The easiest way to run the application is with Docker Compose:

```bash
docker-compose up
```

This will build the Docker image and start the container. The API will be available at `http://localhost:8001`.

### Using Docker Directly

You can also build and run the Docker image directly:

```bash
# Build the image
docker build -t library-api .

# Run the container
docker run -p 8001:8001 -v $(pwd)/data:/app/data -e DATABASE_URL=sqlite:///data/library.db -e ENVIRONMENT=production library-api
```

## API Endpoints

### Health and Version
- `GET /health` - Health check endpoint
- `GET /version` - Get API version

### Authors
- `GET /api/authors/` - Get all authors
- `GET /api/authors/{id}` - Get author by ID
- `GET /api/authors/{id}/books` - Get author with all their books
- `GET /api/authors/{id}/stats` - Get author with book statistics
- `POST /api/authors/` - Create a new author
- `PATCH /api/authors/{id}` - Update an author
- `DELETE /api/authors/{id}` - Delete an author

### Books
- `GET /api/books/` - Get all books
- `GET /api/books/available` - Get available books
- `GET /api/books/by-author/{author_id}` - Get books by author
- `GET /api/books/by-genre/{genre}` - Get books by genre
- `GET /api/books/availability-summary` - Get book availability summary
- `GET /api/books/{id}` - Get book by ID
- `GET /api/books/{id}/with-author` - Get book with author details
- `POST /api/books/` - Create a new book
- `PATCH /api/books/{id}` - Update a book
- `DELETE /api/books/{id}` - Delete a book

### Users
- `GET /api/users/` - Get all users
- `GET /api/users/{id}` - Get user by ID
- `GET /api/users/{id}/loans` - Get user with loans
- `POST /api/users/` - Create a new user
- `PATCH /api/users/{id}` - Update a user
- `DELETE /api/users/{id}` - Delete a user

### Loans
- `GET /api/loans/` - Get all loans
- `GET /api/loans/{id}` - Get loan by ID
- `POST /api/loans/` - Create a new loan
- `PATCH /api/loans/{id}` - Update a loan
- `DELETE /api/loans/{id}` - Delete a loan

## Database Cleaning

To clean the database for testing purposes, run:

```bash
python clean_db.py
```

## Architecture

This application follows a layered architecture:

1. **Presentation Layer**: API routes and views (`app/api/routes/`)
2. **Application Layer**: Services with business logic (`app/services/`)
3. **Domain Layer**: Models and schemas (`app/models/`, `app/schemas/`)
4. **Data Access Layer**: Database sessions and configuration (`app/db/`)

## Documentation

- Database diagrams: See `docs/database_diagram.md`
- Integration diagrams: See `docs/integration_diagram.md`
- Testing endpoints: See `docs/testing_endpoints.md`