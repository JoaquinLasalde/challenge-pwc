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

3. Initialize the database with sample data
```bash
poetry run python -m app.db.init
```

4. Run the application
```bash
poetry run python run.py
```

The API will be available at `http://localhost:8001`

## API Documentation

Once the application is running, you can access:
- Swagger UI: `http://localhost:8001/docs`
- ReDoc: `http://localhost:8001/redoc`

## Project Structure

The application follows a layered architecture:
- `app/api/routes` - API routes (endpoints)
- `app/services` - Business logic
- `app/models` - Database models
- `app/schemas` - API schemas (Pydantic models)
- `app/db` - Database configuration
- `app/core` - Core application configuration
- `docs/` - Documentation including database diagrams and integration examples

## Features

- Health and version endpoints
- Library management (Books, Authors, Users, Loans)
- Full CRUD operations for all resources
- Business logic transformations
- Data transformation between DB and API responses

## Documentation

- [Database Diagram](docs/database_diagram.md) - ER diagram of the database structure using Mermaid
- [Integration Diagram](docs/integration_diagram.md) - Sequence diagram showing potential integration with a notification system
- [Testing Endpoints](docs/testing_endpoints.md) - Examples of how to test all the API endpoints

## Development Process

The application was developed following these steps:

1. Initial project setup with Poetry for dependency management
2. Database model definition using SQLModel
3. Schema definition for API responses using Pydantic models
4. Implementation of core service layer with business logic
5. Creation of API routes for all resources
6. Sample data creation for testing
7. Documentation with diagrams and examples

## Business Requirements

The application implements several business requirements:

1. **Book Availability Management**: 
   - Books can only be loaned if they have available copies
   - When loaned, the available copies count decreases
   - When returned, the available copies count increases

2. **Data Transformations**:
   - Statistics generation for authors, books, users, and loans
   - Relationship-based data enrichment (books with author details, etc.)
   - Complex filtering (overdue loans, users with active loans)

3. **Stateless API Design**:
   - All operations are stateless and can handle concurrent requests
   - Dependencies are injected for each request 