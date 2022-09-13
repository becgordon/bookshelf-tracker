"""CRUD operations."""

from model import db, User, connect_to_db
# Book, Review, Category

# Helper functions here

if __name__ == "__main__":
    from server import app

    connect_to_db(app)