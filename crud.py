"""CRUD operations."""

from model import db, User, Book, Review, Category, Trigger, connect_to_db

# Helper functions here

if __name__ == "__main__":
    from server import app

    connect_to_db(app)