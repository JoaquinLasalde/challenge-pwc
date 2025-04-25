from datetime import date, timedelta
from app.models.author import Author
from app.models.book import Book
from app.models.user import User
from app.models.loan import Loan

# Sample data for Authors
def create_authors():
    return [
        Author(
            name="George Orwell",
            biography="Eric Arthur Blair, known by his pen name George Orwell, was an English novelist, essayist, journalist, and critic.",
            birth_year=1903
        ),
        Author(
            name="J.K. Rowling",
            biography="Joanne Rowling, better known by her pen name J. K. Rowling, is a British author and philanthropist.",
            birth_year=1965
        ),
        Author(
            name="Gabriel García Márquez",
            biography="Gabriel José de la Concordia García Márquez was a Colombian novelist, short-story writer, screenwriter, and journalist.",
            birth_year=1927
        ),
        Author(
            name="Agatha Christie",
            biography="Dame Agatha Mary Clarissa Christie, Lady Mallowan, was an English writer known for her 66 detective novels.",
            birth_year=1890
        )
    ]

# Sample data for Books
def create_books(authors):
    return [
        Book(
            title="1984",
            isbn="9780451524935",
            publication_year=1949,
            genre="Dystopian",
            description="A dystopian social science fiction novel set in a totalitarian state.",
            available_copies=5,
            author_id=authors[0].id
        ),
        Book(
            title="Animal Farm",
            isbn="9780451526342",
            publication_year=1945,
            genre="Political Satire",
            description="An allegorical novella about a group of farm animals who rebel against their human farmer.",
            available_copies=3,
            author_id=authors[0].id
        ),
        Book(
            title="Harry Potter and the Philosopher's Stone",
            isbn="9780747532743",
            publication_year=1997,
            genre="Fantasy",
            description="The first novel in the Harry Potter series that follows a young wizard's journey.",
            available_copies=8,
            author_id=authors[1].id
        ),
        Book(
            title="Harry Potter and the Chamber of Secrets",
            isbn="9780747538486",
            publication_year=1998,
            genre="Fantasy",
            description="The second novel in the Harry Potter series.",
            available_copies=7,
            author_id=authors[1].id
        ),
        Book(
            title="One Hundred Years of Solitude",
            isbn="9780060883287",
            publication_year=1967,
            genre="Magical Realism",
            description="The novel tells the story of the Buendía family over seven generations.",
            available_copies=2,
            author_id=authors[2].id
        ),
        Book(
            title="Murder on the Orient Express",
            isbn="9780062693662",
            publication_year=1934,
            genre="Mystery",
            description="A detective novel featuring the Belgian detective Hercule Poirot.",
            available_copies=4,
            author_id=authors[3].id
        )
    ]

# Sample data for Users
def create_users():
    return [
        User(
            username="john_doe",
            email="john.doe@example.com",
            full_name="John Doe"
        ),
        User(
            username="jane_smith",
            email="jane.smith@example.com",
            full_name="Jane Smith"
        ),
        User(
            username="bob_johnson",
            email="bob.johnson@example.com",
            full_name="Bob Johnson"
        )
    ]

# Sample data for Loans
def create_loans(books, users):
    today = date.today()
    return [
        Loan(
            book_id=books[0].id,
            user_id=users[0].id,
            due_date=today + timedelta(days=14),
            is_returned=False
        ),
        Loan(
            book_id=books[2].id,
            user_id=users[1].id,
            due_date=today + timedelta(days=14),
            is_returned=False
        ),
        Loan(
            book_id=books[4].id,
            user_id=users[2].id,
            due_date=today - timedelta(days=7),
            return_date=today - timedelta(days=2),
            is_returned=True
        )
    ]

def init_db_data(db):
    """Initialize the database with sample data"""
    # Create authors
    authors = create_authors()
    db.add_all(authors)
    db.commit()
    
    # Create books
    books = create_books(authors)
    db.add_all(books)
    db.commit()
    
    # Create users
    users = create_users()
    db.add_all(users)
    db.commit()
    
    # Create loans
    loans = create_loans(books, users)
    db.add_all(loans)
    db.commit()
    
    return {
        "authors": len(authors),
        "books": len(books),
        "users": len(users),
        "loans": len(loans)
    } 