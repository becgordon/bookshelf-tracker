"""Script to seed database."""

import os
import json
import random

import crud
import model
import server

os.system("dropdb bookshelf")
os.system("createdb bookshelf")

model.connect_to_db(server.app)
model.db.create_all()

# Load book data from books.json
with open("data/books.json") as books:
    book_data = json.loads(books.read())

# Create books to store in database
books_db = []
for book in book_data:
    isbn, title, author, description, genre, image, volume_id = (
        book['isbn'],
        book['title'],
        str(book['author']),
        book['description'],
        str(book['genre']),
        book['image'],
        book['volume_id']
    )

    book = crud.create_book(isbn, title, author, description, genre, image, volume_id)
    books_db.append(book)

model.db.session.add_all(books_db)
model.db.session.commit()

# Load user data from users.json
with open("data/users.json") as users:
    users_data = json.loads(users.read())

#create users to store in database
for user in users_data:
    fname, lname, username, profile_image = (
        user['fname'],
        user['lname'],
        user['username'],
        user['profile_image']
    )

    password = 'test'
    user = crud.create_seed_user(fname, lname, username, password, profile_image)
    model.db.session.add(user)
    model.db.session.commit()

    for book in books_db:
        score = random.choice([None,1,2,3,4,5])
        to_be_read = random.choice([True,False])
        favorites = random.choice([True,False])
        review = crud.create_seed_review(user.user_id, 
                                        book.isbn, 
                                        score, 
                                        to_be_read, 
                                        favorites)

        model.db.session.add(review)
        model.db.session.commit()