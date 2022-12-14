"""CRUD operations."""

from model import Password_Reset, db, User, Book, Review, connect_to_db
import re

# FUNCTIONS FOR USERS TABLE --------------------------------------------------

def create_user(fname, lname, email, username, password):
    """Create and return a new user."""
    
    user = User(fname=fname, 
                lname=lname, 
                email=email,
                username=username, 
                password=password)
    
    return user


def create_seed_user(fname, lname, email, username, password, profile_image):
    """Create a user specifically for seed_database.py."""

    user = User(fname=fname, 
            lname=lname, 
            username=username, 
            password=password,
            email=email,
            profile_image=profile_image)
    
    return user


def get_user_by_username(username):
    """Get a user by username."""

    return User.query.filter(User.username == username).first()


def get_user_by_email(email):
    """Get a user by email."""

    return User.query.filter(User.email == email).first()


def get_all_viewable_users(user):
    """Get all users."""

    return User.query.filter((User.profile_view == True) & (User.username != user.username)).all()


def is_password_strong(password):
    """Check if a password meets requirements."""
    
    upper_alpha = 0
    lower_alpha = 0
    numeric = 0
    
    for character in password:
        if character.isalpha() and character.isupper():
            upper_alpha += 1
        if character.isalpha() and character.islower():
            lower_alpha += 1
        if character.isnumeric():
            numeric += 1
    
    if upper_alpha > 0 and lower_alpha > 0 and numeric > 0:
        return True
    else:
        return False



# FUNCTIONS FOR BOOKS TABLE --------------------------------------------------


def create_book(isbn, title, author, description, genre, image, volume_id):
    """Create and return a new book."""

    book = Book(isbn=isbn,
                title=title,
                author=author,
                description=description,
                genre=genre,
                image=image,
                volume_id=volume_id)
    
    return book

def get_book_by_isbn(isbn):
    """Get a book by ISBN."""

    return Book.query.filter(Book.isbn == isbn).first()


def sort_json_response(response):
    """Take in a Google Books JSON request and sort it into variables."""

    title = response['volumeInfo']['title']
    if 'authors' in response['volumeInfo']:
        author = ' '.join(response['volumeInfo']['authors'])
    else:
        author = None
    image = response['volumeInfo']['imageLinks']['thumbnail']
    if 'categories' in response['volumeInfo']:
        genre = ' '.join(response['volumeInfo']['categories'])
    else:
        genre = None
    if 'industryIdentifiers' in response['volumeInfo']:
        isbn = ''.join(response['volumeInfo']['industryIdentifiers'][1]['identifier'])
    else:
        isbn = None
    description = re.sub("<.>|<..>", "", response['volumeInfo']['description'])
    volume_id = response['id']

    return title, author, image, genre, isbn, description, volume_id


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


def create_seed_review(user_id, isbn, score, to_be_read, favorites):
    """Create a review specifically for seed_database.py."""

    review = Review(user_id=user_id, 
                    isbn=isbn, 
                    score=score, 
                    to_be_read=to_be_read,
                    favorites=favorites)

    return review


def does_review_exist(user_id, isbn):
    """Check if a user has a review for a particular book."""
    
    return bool(Review.query.filter((Review.user_id == user_id) & (Review.isbn == isbn)).first())


def get_review_by_book_and_user_id(isbn, user_id):
    """Get a review ID by ISBN and user ID."""

    return Review.query.filter((Review.user_id == user_id) & (Review.isbn == isbn)).first()


# FUNCTIONS FOR PASSWORDRESETS TABLE -----------------------------------------


def create_password_reset(reset_id, email):
    """Create a password reset."""

    password_reset = Password_Reset(reset_id=reset_id, email=email)

    return password_reset


def get_reset_by_reset_id(reset_id):
    """Get email by reset_id."""

    reset = Password_Reset.query.filter(Password_Reset.reset_id == reset_id).first()

    return reset


# ----------------------------------------------------------------------------

if __name__ == "__main__":
    from server import app
    connect_to_db(app)