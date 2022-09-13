"""CRUD operations."""

from model import db, User, Book, Review, Category, BookCategory, connect_to_db

def create_user(fname, lname, username, password):
    """Create and return a new user."""
    
    user = User(fname=fname, 
                lname=lname, 
                username=username, 
                password=password)
    
    return user

def create_book(isbn, title, author, description, genre, image):
    """Create and return a new book."""
    
    book = Book(isbn=isbn,
                title=title,
                author=author,
                description=description,
                genre=genre,
                image=image)
    
    return book

def create_review(score, review_text, user_id, isbn):
    """Create and return a new review."""
    
    review = Review(score=score,
                    review_text=review_text,
                    user_id=user_id,
                    isbn=isbn)

    return review

def create_category(category):
    """Creates and returns a new category."""

    category = Category(category=category)

    return category

if __name__ == "__main__":
    from server import app
    connect_to_db(app)