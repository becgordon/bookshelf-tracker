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
    isbn, title, author, description, genre, image = (
        book['isbn'],
        book['title'],
        str(book['author']),
        book['description'],
        str(book['genre']),
        book['image']
    )

    book = crud.create_book(isbn, title, author, description, genre, image)
    books_db.append(book)

model.db.session.add_all(books_db)
model.db.session.commit()

# create 3 users and give each user three books
for n in range(0,6):
    fname = f'first{n}'
    lname = f'last{n}'
    username = f'username{n}'
    password = 'test'

    user = crud.create_user(fname, lname, username, password)
    model.db.session.add(user)

    for num in range(0,4):
        book = random.choice(books_db)
        score = random.randint(1,5)
        review_text = "N/A"

        review = crud.create_review(score, user.user_id, book.isbn)
        model.db.session.add(review)

model.db.session.commit()