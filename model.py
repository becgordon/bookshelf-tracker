"""Models for bookshelf tracking app."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


# CLASS USER -----------------------------------------------------------------


class User(db.Model):
    """A user."""
    
    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    fname = db.Column(db.String(25), nullable=False)
    lname = db.Column(db.String(25), nullable=False)
    username = db.Column(db.String(25), nullable=False, unique=True)
    password = db.Column(db.String(50), nullable=False)

    reviews = db.relationship('Review', back_populates='user') 

    def __repr__(self):
        """Show info about user."""

        return f'<User user_id={self.user_id} name={self.fname} {self.lname}>'


# CLASS BOOK -----------------------------------------------------------------


class Book(db.Model):
    """A book."""

    __tablename__ = 'books'

    isbn = db.Column(db.String, primary_key=True)
    title = db.Column(db.String)
    author = db.Column(db.String)
    description = db.Column(db.Text)
    genre = db.Column(db.String)
    image = db.Column(db.String)
    
    reviews = db.relationship("Review", back_populates="book") 
    
    # categories = db.relationship('Category', 
    #                             secondary="books_categories", 
    #                             back_populates="books")

    def __repr__(self):
        """Show info about book."""

        return f'<Book isbn={self.isbn} title={self.title}>'


# CLASS REVIEW ---------------------------------------------------------------


class Review(db.Model):
    """A review."""
    
    __tablename__ = 'reviews'

    review_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    score = db.Column(db.Integer)
    to_be_read = db.Column(db.Boolean)
    favorites = db.Column(db.Boolean)

    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    isbn = db.Column(db.String, db.ForeignKey('books.isbn'))

    book = db.relationship("Book", back_populates="reviews")
    user = db.relationship("User", back_populates="reviews")

    def __repr__(self):
        """Show info about review."""

        return f'<Review review_id={self.review_id} user_id={self.user_id}>'


# CLASS CATEGORY -------------------------------------------------------------


# class Category(db.Model):
#     """A category of book."""
#     __tablename__ = 'categories'

#     category_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     category = db.Column(db.String)

#     books = db.relationship("Book", 
#                             secondary="books_categories", 
#                             back_populates='categories')

#     def __repr__(self):
#         """Show info about a category."""

#         return f'<Category category_id={self.category_id} {self.category}>'


# # ASSOCIATION TABLES ---------------------------------------------------------

# class BookCategory(db.Model):
#     """Category of a specific book."""

#     __tablename__ = 'books_categories'

#     book_category_id = db.Column(db.Integer, primary_key=True)
#     isbn = db.Column(db.String, db.ForeignKey("books.isbn"), nullable=False)
#     category_id = db.Column(db.Integer, 
#                             db.ForeignKey("categories.category_id"), 
#                             nullable=False)
    
#     def __repr__(self):
#         """Show info about a BookCategory."""

#         return f'<BookCategory isbn={self.isbn} category_id={self.category_id}>'


# 2.0 FEATURES ---------------------------------------------------------------


# class Trigger(db.Model): # 2.0 Feature
#     """A trigger warning for book."""
#     pass


# class BookTrigger(db.Model): # 2.0 Feature
#     """Trigger of a specific book."""
#     pass


# ----------------------------------------------------------------------------


def connect_to_db(app, db_uri="postgresql:///bookshelf"):
    """Connect to database."""

    app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    app.config["SQLALCHEMY_ECHO"] = True
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.app = app
    db.init_app(app)

    print("Connected to db.")


if __name__ == "__main__":
    from server import app

    connect_to_db(app)
