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
    email = db.Column(db.String, nullable=False)
    username = db.Column(db.String(25), nullable=False, unique=True)
    password = db.Column(db.String(50), nullable=False)
    profile_image = db.Column(db.String, server_default='/static/images/default_profile.png')
    profile_view = db.Column(db.Boolean, server_default='True')

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
    volume_id = db.Column(db.String)
    
    reviews = db.relationship("Review", back_populates="book") 

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
    current_read = db.Column(db.Boolean, server_default='False')

    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    isbn = db.Column(db.String, db.ForeignKey('books.isbn'))

    book = db.relationship("Book", back_populates="reviews")
    user = db.relationship("User", back_populates="reviews")

    def __repr__(self):
        """Show info about review."""

        return f'<Review review_id={self.review_id} user_id={self.user_id}>'


# CLASS PASSWORD_RESET -------------------------------------------------------


class Password_Reset(db.Model):
    """Password reset."""

    __tablename__ = 'passwordresets'

    password_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    reset_id = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)

    def __repr__(self):
        """Show info about passsword reset."""

        return f'<Password_Reset reset_id={self.reset_id} email={self.email}>'


# EXAMPLE DATA ---------------------------------------------------------------


def example_data():
    """Create some sample data for testing."""

    User.query.delete()
    Book.query.delete()
    Review.query.delete()

    # Example Users
    JackT = User(fname='Jack', 
                lname='Torrance', 
                email='JackT@test.com',
                username='JackT',
                password='test',
                profile_image="/static/images/JackT.jpg",
                profile_view=True)

    BevM = User(fname='Beverly', 
                lname='Marsh', 
                email='BevM@test.com',
                username='BevM',
                password='test',
                profile_image="/static/images/BevM.jpg",
                profile_view=True)

    PaulE = User(fname='Paul', 
                lname='Edgecomb', 
                email='PaulE@test.com',
                username='PaulE',
                password='test',
                profile_image="/static/images/PaulE.jpg",
                profile_view=False)

    # Example Books
    book1 = Book(isbn="123",
                title="If It Bleeds",
                author="Stephen King",
                description="test description",
                genre="Fiction",
                image='test image',
                volume_id='123')

    book2 = Book(isbn="456",
                title="Elevation",
                author="Stephen King",
                description="test description",
                genre="Fiction",
                image='test image',
                volume_id='456')

    book3 = Book(isbn="789",
                title="Phantoms",
                author="Dean Koontz",
                description="test description",
                genre="Horror",
                image='test image',
                volume_id='789')

    # Example Reviews  

    review1 = Review(score=3,
                    to_be_read=False,
                    favorites=True,
                    current_read=False,
                    user_id=1,
                    isbn="123")

    review2 = Review(score=4,
                    to_be_read=True,
                    favorites=False,
                    current_read=False,
                    user_id=1,
                    isbn="456")

    review3 = Review(score=5,
                    to_be_read=True,
                    favorites=False,
                    current_read=True,
                    user_id=1,
                    isbn="789")

    db.session.add_all([JackT, BevM, PaulE, book1, book2, book3])
    db.session.commit()
    db.session.add_all([review1, review2, review3])
    db.session.commit()


# ----------------------------------------------------------------------------


def connect_to_db(app, db_uri="postgresql:///bookshelf"):
    """Connect to database."""

    app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    app.config["SQLALCHEMY_ECHO"] = True
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    

if __name__ == "__main__":
    from server import app
    connect_to_db(app)
    print("Connected to db.")
