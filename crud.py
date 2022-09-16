"""CRUD operations."""

from model import db, User, Book, Review, Category, BookCategory, connect_to_db

def create_user(fname, lname, username, password):
    """Create and return a new user."""
    
    user = User(fname=fname, 
                lname=lname, 
                username=username, 
                password=password)
    
    return user

def get_user_by_username(username):
    """Get a user by username."""

    return User.query.filter(User.username == username).first()


def get_user_by_user_id(user_id):
    """Get a user by user ID."""

    return User.query.filter(User.user_id == user_id).first()


def get_book_by_isbn(isbn):
    """Get a book by ISBN."""

    return Book.query.get(isbn)


def create_book(isbn, title, author, description, genre, image):
    """Create and return a new book."""

    book = Book(isbn=isbn,
                title=title,
                author=author,
                description=description,
                genre=genre,
                image=image)
    
    return book

def create_review(score, user_id, isbn):
    """Create and return a new review."""
    
    review = Review(score=score,
                    user_id=user_id,
                    isbn=isbn)

    return review

def get_review_by_user_id(user_id):
    """Get a review by user ID."""

    return Review.query.get(user_id)

def create_category(category):
    """Creates and returns a new category."""

    category = Category(category=category)

    return category

if __name__ == "__main__":
    from server import app
    connect_to_db(app)