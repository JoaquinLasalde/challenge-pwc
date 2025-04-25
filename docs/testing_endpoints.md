# Testing the API Endpoints

This document provides examples of how to test all the endpoints in the Library Management API using `curl`. These examples use the default port 8001.

## Health and Version Endpoints

```bash
# Check health
curl -s http://localhost:8001/health | python -m json.tool

# Check version
curl -s http://localhost:8001/version | python -m json.tool
```

## Authors Endpoints

```bash
# Get all authors
curl -s http://localhost:8001/api/authors/ | python -m json.tool

# Get author by ID (replace {id} with an actual UUID)
curl -s http://localhost:8001/api/authors/{id} | python -m json.tool

# Get author with books
curl -s http://localhost:8001/api/authors/{id}/books | python -m json.tool

# Get author statistics (business transformation example)
curl -s http://localhost:8001/api/authors/{id}/stats | python -m json.tool

# Create a new author
curl -s -X POST -H "Content-Type: application/json" \
  -d '{"name": "New Author", "biography": "Biography text", "birth_year": 1980}' \
  http://localhost:8001/api/authors/ | python -m json.tool

# Update an author
curl -s -X PATCH -H "Content-Type: application/json" \
  -d '{"biography": "Updated biography"}' \
  http://localhost:8001/api/authors/{id} | python -m json.tool

# Delete an author
curl -s -X DELETE http://localhost:8001/api/authors/{id} | python -m json.tool
```

## Books Endpoints

```bash
# Get all books
curl -s http://localhost:8001/api/books/ | python -m json.tool

# Get available books (business logic filtering)
curl -s http://localhost:8001/api/books/available | python -m json.tool

# Get books by author
curl -s http://localhost:8001/api/books/by-author/{author_id} | python -m json.tool

# Get books by genre
curl -s http://localhost:8001/api/books/by-genre/Fantasy | python -m json.tool

# Get book availability summary (business transformation)
curl -s http://localhost:8001/api/books/availability-summary | python -m json.tool

# Get book by ID
curl -s http://localhost:8001/api/books/{id} | python -m json.tool

# Get book with author details
curl -s http://localhost:8001/api/books/{id}/with-author | python -m json.tool

# Create a new book
curl -s -X POST -H "Content-Type: application/json" \
  -d '{"title": "New Book", "isbn": "1234567890123", "publication_year": 2023, "genre": "Sci-Fi", "description": "A new book", "available_copies": 5, "author_id": "{author_id}"}' \
  http://localhost:8001/api/books/ | python -m json.tool

# Update a book
curl -s -X PATCH -H "Content-Type: application/json" \
  -d '{"available_copies": 10}' \
  http://localhost:8001/api/books/{id} | python -m json.tool

# Delete a book
curl -s -X DELETE http://localhost:8001/api/books/{id} | python -m json.tool
```

## Users Endpoints

```bash
# Get all users
curl -s http://localhost:8001/api/users/ | python -m json.tool

# Get users with active loans (business logic filtering)
curl -s http://localhost:8001/api/users/with-active-loans | python -m json.tool

# Get user by ID
curl -s http://localhost:8001/api/users/{id} | python -m json.tool

# Get user with loans
curl -s http://localhost:8001/api/users/{id}/loans | python -m json.tool

# Get user activity summary (business transformation)
curl -s http://localhost:8001/api/users/{id}/activity | python -m json.tool

# Create a new user
curl -s -X POST -H "Content-Type: application/json" \
  -d '{"username": "newuser", "email": "user@example.com", "full_name": "New User"}' \
  http://localhost:8001/api/users/ | python -m json.tool

# Update a user
curl -s -X PATCH -H "Content-Type: application/json" \
  -d '{"email": "updated@example.com"}' \
  http://localhost:8001/api/users/{id} | python -m json.tool

# Delete a user
curl -s -X DELETE http://localhost:8001/api/users/{id} | python -m json.tool
```

## Loans Endpoints

```bash
# Get all loans
curl -s http://localhost:8001/api/loans/ | python -m json.tool

# Get overdue loans (business logic filtering)
curl -s http://localhost:8001/api/loans/overdue | python -m json.tool

# Get loan statistics (business transformation)
curl -s http://localhost:8001/api/loans/statistics | python -m json.tool

# Get loan by ID
curl -s http://localhost:8001/api/loans/{id} | python -m json.tool

# Get loan with details
curl -s http://localhost:8001/api/loans/{id}/details | python -m json.tool

# Create a new loan (includes business logic to check book availability)
curl -s -X POST -H "Content-Type: application/json" \
  -d '{"book_id": "{book_id}", "user_id": "{user_id}", "due_date": "2025-05-15"}' \
  http://localhost:8001/api/loans/ | python -m json.tool

# Mark a book as returned (includes business logic to update book availability)
curl -s -X POST http://localhost:8001/api/loans/{id}/return | python -m json.tool

# Update a loan
curl -s -X PATCH -H "Content-Type: application/json" \
  -d '{"due_date": "2025-06-01"}' \
  http://localhost:8001/api/loans/{id} | python -m json.tool

# Delete a loan
curl -s -X DELETE http://localhost:8001/api/loans/{id} | python -m json.tool
```

## Using the Swagger UI

You can also test all endpoints using the built-in Swagger UI at `http://localhost:8001/docs`. This provides:

1. Interactive documentation
2. Example requests for all endpoints
3. Schema information for all data models
4. The ability to execute requests directly from the browser

## Required Functionality Demos

To demonstrate the required functionality of the API:

1. **Business Transformation in Service Layer**:
   - `/api/authors/{id}/stats` - Author statistics
   - `/api/books/availability-summary` - Book availability summary
   - `/api/users/{id}/activity` - User activity summary
   - `/api/loans/statistics` - Loan statistics

2. **Data Transformation Between DB and API**:
   - Compare the DB model fields with the API response fields
   - Note the different structure in extended endpoints like `/books/{id}/with-author`

3. **Stateless API Handling Multiple Users**:
   - The API uses no session state
   - FastAPI handles concurrent requests efficiently
   - Dependencies are injected for each request 