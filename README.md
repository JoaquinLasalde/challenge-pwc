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
- `GET /api/v1/authors/` - Get all authors
- `GET /api/v1/authors/{id}` - Get author by ID
- `GET /api/v1/authors/{id}/books` - Get author with all their books
- `GET /api/v1/authors/{id}/stats` - Get author with book statistics
- `POST /api/v1/authors/` - Create a new author
- `PATCH /api/v1/authors/{id}` - Update an author
- `DELETE /api/v1/authors/{id}` - Delete an author

### Books
- `GET /api/v1/books/` - Get all books
- `GET /api/v1/books/available` - Get available books
- `GET /api/v1/books/by-author/{author_id}` - Get books by author
- `GET /api/v1/books/by-genre/{genre}` - Get books by genre
- `GET /api/v1/books/availability-summary` - Get book availability summary
- `GET /api/v1/books/{id}` - Get book by ID
- `GET /api/v1/books/{id}/with-author` - Get book with author details
- `POST /api/v1/books/` - Create a new book
- `PATCH /api/v1/books/{id}` - Update a book
- `DELETE /api/v1/books/{id}` - Delete a book

### Users
- `GET /api/v1/users/` - Get all users
- `GET /api/v1/users/{id}` - Get user by ID
- `GET /api/v1/users/{id}/loans` - Get user with loans
- `POST /api/v1/users/` - Create a new user
- `PATCH /api/v1/users/{id}` - Update a user
- `DELETE /api/v1/users/{id}` - Delete a user

### Loans
- `GET /api/v1/loans/` - Get all loans
- `GET /api/v1/loans/{id}` - Get loan by ID
- `POST /api/v1/loans/` - Create a new loan
- `PATCH /api/v1/loans/{id}` - Update a loan
- `DELETE /api/v1/loans/{id}` - Delete a loan

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

## Logging

The application includes a comprehensive logging system:

- **Log Levels**: Automatically adjusts based on environment (DEBUG for testing, INFO for development, WARNING for production)
- **Log Rotation**: Logs are stored in `logs/` directory with rotation (10MB per file, max 5 files)
- **Request Tracking**: Each HTTP request gets a unique ID for tracing through the system
- **Performance Monitoring**: Request processing time is logged
- **Structured Logs**: Logs include timestamps, levels, and originating components

To access logs:

- Console logs: Visible in the terminal output
- File logs: Located in the `logs/` directory

## Error Handling

The application implements the Problem Details for HTTP APIs standard (RFC 9457):

- **Standardized Error Format**: All errors follow a consistent JSON structure
- **Rich Error Information**: Errors include type, title, status, detail, and instance fields
- **Detailed Validation Errors**: Input validation errors include field-specific information
- **Reference Links**: Error types include URI references to detailed documentation

Example error response:

```json
{
  "type": "https://httpstatuses.com/404",
  "title": "Not Found",
  "status": 404,
  "detail": "The author with ID 123e4567-e89b-12d3-a456-426614174000 was not found",
  "instance": "/api/v1/authors/123e4567-e89b-12d3-a456-426614174000"
}
```

## Correlation IDs

The application implements a correlation ID system for request tracing:

- **Unique Request Identifier**: Each request is assigned a UUID
- **Header Propagation**: Correlation IDs are passed via the `X-Correlation-ID` header
- **Distributed Tracing**: Existing IDs from upstream services are preserved
- **Request Context**: Correlation IDs are available throughout the request lifecycle
- **Performance Tracking**: Response times are tracked and returned via the `X-Process-Time-Ms` header

This feature allows tracking requests across multiple services and provides better observability for debugging and monitoring.

## Documentation

- Database diagrams: See `docs/database_diagram.md`
- Integration diagrams: See `docs/integration_diagram.md`
- Testing endpoints: See `docs/testing_endpoints.md`