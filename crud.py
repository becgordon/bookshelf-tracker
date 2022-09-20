"""CRUD operations."""

from model import db, User, Book, Review, Category, BookCategory, connect_to_db

# FUNCTIONS FOR USERS TABLE --------------------------------------------------

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


# FUNCTIONS FOR BOOKS TABLE --------------------------------------------------


def create_book(isbn, title, author, description, genre, image):
    """Create and return a new book."""

    book = Book(isbn=isbn,
                title=title,
                author=author,
                description=description,
                genre=genre,
                image=image)
    
    return book

def get_book_by_isbn(isbn):
    """Get a book by ISBN."""

    return Book.query.filter(Book.isbn == isbn).first()
    # return Book.query.get(isbn)


def get_book_by_review_id(review_id):
    """Get a book by review ID."""

    review = Review.query.filter(Review.review_id == review_id).first()
    return review.book 


# SORTING BOOKS --------------------------------------------------------------


def sort_books_alphabetically_title(user): 
    """Sort a user's books alphabetically by title."""

    reviews = user.reviews
    reviews = reviews.sort(key=lambda x: x.book.title)
    
    return reviews


def sort_books_alphabetically_author(user): 
    """Sort a user's books alphabetically by author."""

    reviews = user.reviews
    reviews = reviews.sort(key=lambda x: x.book.author)
    
    return reviews


def sort_books_most_recently_added(user): 
    """Sort a user's books by most recently added."""

    reviews = user.reviews
    reviews = reviews.sort(key=lambda x: x.review_id, reverse=True)
    
    return reviews


def sort_books_least_recently_added(user): 
    """Sort a user's books by most recently added."""

    reviews = user.reviews
    reviews = reviews.sort(key=lambda x: x.review_id)
    
    return reviews


# FUNCTIONS FOR REVIEWS TABLE ------------------------------------------------


def create_review(user_id, isbn):
    """Create and return a new review."""
    
    review = Review(user_id=user_id, isbn=isbn)

    return review


def get_review_by_user_id(user_id):
    """Get reviews by user ID."""

    return Review.query.filter(Review.user_id == user_id).all() 


def does_review_exist(user_id, isbn):
    """Check if a user has a review for a particular book."""
    
    return bool(Review.query.filter((Review.user_id == user_id) & (Review.isbn == isbn)).first())


def get_review_by_book_and_user_id(isbn, user_id):
    """Get a review ID by ISBN and user ID."""

    return Review.query.filter((Review.user_id == user_id) & (Review.isbn == isbn)).first()


# FUNCTIONS FOR CATEGORIES TABLE ---------------------------------------------

def create_category(category):
    """Creates and returns a new category."""

    category = Category(category=category)

    return category


def add_category_to_book(book):
    """Add a category to a book."""
    pass

# ----------------------------------------------------------------------------

if __name__ == "__main__":
    from server import app
    connect_to_db(app)


# TESTING --------------------------------------------------------------------