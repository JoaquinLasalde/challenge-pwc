# Database Diagram

The library management system consists of four main entities: Authors, Books, Users, and Loans.

## ER Diagram

```mermaid
erDiagram
    AUTHOR ||--o{ BOOK : writes
    BOOK ||--o{ LOAN : borrowed_in
    USER ||--o{ LOAN : borrows
    
    AUTHOR {
        UUID id PK
        string name
        string biography
        int birth_year
        datetime created_at
        datetime updated_at
    }
    
    BOOK {
        UUID id PK
        string title
        string isbn UK
        int publication_year
        string genre
        string description
        int available_copies
        UUID author_id FK
        datetime created_at
        datetime updated_at
    }
    
    USER {
        UUID id PK
        string username UK
        string email UK
        string full_name
        boolean is_active
        datetime created_at
        datetime updated_at
    }
    
    LOAN {
        UUID id PK
        date loan_date
        date due_date
        date return_date
        boolean is_returned
        UUID book_id FK
        UUID user_id FK
        datetime created_at
        datetime updated_at
    }
```

## Relationships

1. **Author - Book**: One-to-Many
   - An author can write multiple books
   - Each book has exactly one author

2. **Book - Loan**: One-to-Many
   - A book can be loaned multiple times (sequentially)
   - Each loan refers to exactly one book

3. **User - Loan**: One-to-Many
   - A user can borrow multiple books
   - Each loan is associated with exactly one user

## Business Logic Constraints

1. A book can only be loaned if it has available copies (`available_copies > 0`)
2. When a book is loaned, its `available_copies` is decreased by 1
3. When a book is returned, its `available_copies` is increased by 1
4. A book is considered overdue if:
   - The current date is past the `due_date`
   - The book has not been returned (`is_returned = false`) 