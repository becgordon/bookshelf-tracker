"""Models for bookshelf tracking app."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    """A user."""
    pass

class Book(db.Model):
    """A book."""
    pass

class Review(db.Model):
    """A review."""
    pass

class Category(db.Model):
    """A category of book."""
    pass

class Trigger(db.Model):
    """A trigger warning for book."""
    pass

def connect_to_db(flask_app, db_uri="postgresql://bookshelf", echo=True):
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    flask_app.config["SQLALCHEMY_ECHO"] = echo
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.app = flask_app
    db.init_app(flask_app)

    print("Connected to db.")

    if __name__ == "__main__":
        from server import app

        connect_to_db(app)