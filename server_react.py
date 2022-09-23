"""Server for bookshelf tracking app."""

from flask import Flask, render_template, request, flash, session, redirect, jsonify
import os
import re
import random
from model import connect_to_db, db
import requests
import crud

from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = "dev"

BOOKS_API_KEY = os.environ['GOOGLE_BOOKS_KEY']

app.jinja_env.undefined = StrictUndefined


#  BASIC ROUTES --------------------------------------------------------------


@app.route('/')
def welcome_page():
    """View welcome page."""
    
    return render_template('welcome_page.html')


# ACCOUNT ROUTES -------------------------------------------------------------


@app.route('/login')
def log_in_page():
    """Allow a user to log in."""

    if session:
        username = session.get("user_name")
        return redirect(f'/userprofile/{username}')

    return render_template('login.html')


@app.route('/login', methods=["POST"])
def log_in():
    """Submits log in info and goes to user profile."""

    username = request.form.get('username')
    password = request.form.get('password')

    user = crud.get_user_by_username(username)

    if not user or user.password != password:
        flash("The email or password entered were incorrect.")
        return redirect('/login')
    else:
        session['user_name'] = user.username
        flash("Successfully logged in!")
        return redirect(f'/userprofile/{user.username}')


@app.route('/createaccount')
def show_create_account():
    """Show form to create an account."""

    return render_template('create_account.html')


@app.route('/createaccount', methods=["POST"])
def create_account():
    """Create a new a account."""

    fname = request.form.get('fname')
    lname = request.form.get('lname')
    username = request.form.get('username')
    password = request.form.get('password')

    user = crud.get_user_by_username(username)

    if user:
        flash("Sorry! That username is already taken.")
    else:
        user = crud.create_user(fname, lname, username, password)
        db.session.add(user)
        db.session.commit()
        flash('Account creation successful!')

    return redirect('/login')


@app.route('/userprofile/<username>')
def view_user_profile(username):
    """View a particular user's profile."""

    user = crud.get_user_by_username(username)

    user_books = []

    if user and 'user_name' in session and session['user_name'] == username:
        for review in user.reviews:
            user_books.append({'title': review.book.title,
                                'author': review.book.author,
                                'image': review.book.image,
                                'isbn': review.book.isbn
                                })
        return jsonify(user_books)
    else:
        return redirect("/login")


@app.route('/logout') 
def log_out():
    """Allow a user to log out."""
    session.clear()
    
    return redirect('/')


# BOOK ROUTES ----------------------------------------------------------------


# @app.route('/booksearchresults')
# def submit_book_search():
#     """Takes in search term an returns results that match."""

#     search_term = request.args.get('search_term')

#     url = 'https://www.googleapis.com/books/v1/volumes'
#     payload = {'apikey': BOOKS_API_KEY, 'q': search_term}
    
#     res = requests.get(url, params=payload)
#     data = res.json()

#     if 'items' in data:
#         books = data['items']
#     else:
#         books = []

#     search_results = []

#     for book in books:
#         isbn = ''.join(book['volumeInfo']['industryIdentifiers'][0]['identifier'])
#         # if not crud.get_book_by_isbn(isbn):
#         title = book['volumeInfo']['title']
#         if 'authors' in book['volumeInfo']:
#             author = ' '.join(book['volumeInfo']['authors'])
#         else:
#             author = None
#         if 'description' in book['volumeInfo']:
#             description = book['volumeInfo']['description']
#             desc_edit = re.sub("<.>|<..>", "", description)
#         else:
#             description = None
#             desc_edit = None
#         if 'categories' in book['volumeInfo']:
#             genre = ' '.join(book['volumeInfo']['categories'])
#         else:
#             genre = None
#         if 'imageLinks' in book['volumeInfo']:
#             image = book['volumeInfo']['imageLinks']['thumbnail']
#         else:
#             image = None

#         search_results.append({'isbn': isbn,
#                                 'title': title,
#                                 'author': author,
#                                 'description': desc_edit,
#                                 'genre': genre,
#                                 'image': image
#                                 })

#     return jsonify(search_results)


@app.route('/booksearchresults')
def submit_book_search():
    """Takes in search term an returns results that match."""

    search_term = request.args.get('search_term')

    url = 'https://www.googleapis.com/books/v1/volumes'
    payload = {'apikey': BOOKS_API_KEY, 'q': search_term}
    
    res = requests.get(url, params=payload)
    data = res.json()

    if 'items' in data:
        books = data['items']
    else:
        books = []
    
    return render_template('book_search_results.html',
                            books=books, 
                            searchterm=search_term)
    

@app.route('/bookprofile/<volume_id>')
def view_book_profile(volume_id):
    """View a particular book's profile."""
    
    url = f'https://www.googleapis.com/books/v1/volumes/{volume_id}'
    payload = {'apikey': BOOKS_API_KEY}
    res = requests.get(url, params=payload)
    profile = res.json()

    description = profile['volumeInfo']['description']
    desc_edit = re.sub("<.>|<..>", "", description)

    return render_template('book_profile.html', profile=profile, desc_edit=desc_edit)


@app.route('/addbook/<volume_id>')
def add_book(volume_id):
    """Adds a book to a particular user's library."""

    url = f'https://www.googleapis.com/books/v1/volumes/{volume_id}'
    payload = {'apikey': BOOKS_API_KEY}

    res = requests.get(url, params=payload)
    book = res.json()

    isbn = ''.join(book['volumeInfo']['industryIdentifiers'][0]['identifier'])
   
    if not crud.get_book_by_isbn(isbn):
        title = book['volumeInfo']['title']
        if 'authors' in book['volumeInfo']:
            author = ' '.join(book['volumeInfo']['authors'])
        else:
            author = None
        description = book['volumeInfo']['description']
        desc_edit = re.sub("<.>|<..>", "", description)
        if 'categories' in book['volumeInfo']:
            genre = ' '.join(book['volumeInfo']['categories'])
        else:
            genre = None
        image = book['volumeInfo']['imageLinks']['thumbnail']
        
        book = crud.create_book(isbn, title, author, desc_edit, genre, image)

        db.session.add(book)

    user = crud.get_user_by_username(session['user_name'])

    if not crud.does_review_exist(user.user_id, isbn):
        review = crud.create_review(user.user_id, isbn)
        db.session.add(review)
        db.session.commit()
    else:
        flash("You've already added this book.")
        
    return redirect(f'/userprofile/{user.username}')


@app.route('/user/userbook<isbn>') 
def edit_book_settings(isbn):
    """Allow a user to edit characteristics of a book in their library."""

    user = crud.get_user_by_username(session['user_name'])
    book = crud.get_book_by_isbn(isbn)
    review = crud.get_review_by_book_and_user_id(isbn, user.user_id)

    return render_template('user_book_profile.html', user=user, book=book, review=review)


@app.route('/removebook<isbn>')
def remove_book(isbn):
    """Removes book from a user's library."""
    
    user = crud.get_user_by_username(session['user_name'])
    review = crud.get_review_by_book_and_user_id(isbn, user.user_id)
    db.session.delete(review)
    db.session.commit()

    return redirect(f'/userprofile/{user.username}')


@app.route('/sortby')
def sort_books():
    """Sorts a user's books by user's selection."""

    user = crud.get_user_by_username(session['user_name'])
    
    sort_by = request.args.get("sort")

    if sort_by == "alphabetical by title":
        crud.sort_books_alphabetically_title(user)
    elif sort_by == "alphabetical by author":
        crud.sort_books_alphabetically_author(user)
    elif sort_by == "most recently added":
        crud.sort_books_most_recently_added(user)
    elif sort_by == "least recently added":
        crud.sort_books_least_recently_added(user)

    return render_template('user_profile.html', user=user)


@app.route('/ratebook<isbn>')
def rate_book(isbn): 
    """Add a user's rating to a book."""

    user = crud.get_user_by_username(session['user_name'])
    rating = request.args.get("rating")
    review = crud.get_review_by_book_and_user_id(isbn, user.user_id)
    review.score = rating
    db.session.commit()

    return redirect(f'/userprofile/{user.username}')


@app.route('/categorizebook<isbn>/<category>') # needs some editing to work as AJAX request
def categorize_book(isbn, category):
    """Categorize a user's book."""

    user = crud.get_user_by_username(session['user_name'])
    review = crud.get_review_by_book_and_user_id(isbn, user.user_id)
    if category == "To Be Read":
        review.to_be_read = True
    elif category == "Have Read":
        review.to_be_read = False
    elif category == "Favorites":
        review.favorites = True
    db.session.commit()

    return f'Your book has been successfully added to your "{category}" shelf!'
    # return redirect(f'/userprofile/{user.username}')


@app.route('/shelf')
def display_shelf():
    """Show user a particular shelf."""

    user = crud.get_user_by_username(session['user_name'])
    shelf = request.args.get("shelf")
    shelf_list = []
    if shelf == "To Be Read":
        for review in user.reviews:
            if review.to_be_read == True:
                shelf_list.append(review)
    elif shelf == "Have Read":
        for review in user.reviews:
            if review.to_be_read == False:
                shelf_list.append(review)
    elif shelf == "Favorite":
        for review in user.reviews:
            if review.favorites == True:
                shelf_list.append(review)
    
    return render_template('user_shelf.html', reviews=shelf_list, shelf=shelf)


@app.route('/usercharts/<username>')
def view_charts(username):
    """Allow a user ot view their library data in a chart."""
    
    user = crud.get_user_by_username(session['user_name'])

    if user and 'user_name' in session and session['user_name'] == username:
        to_be_read = 0
        have_read = 0
        rated = 0
        unrated = 0
        favorites = 0
        for review in user.reviews:
            if review.to_be_read == True:
                to_be_read += 1
            if review.to_be_read == False:
                have_read += 1
            if review.favorites == True:
                favorites += 1
            if review.score == None:
                unrated += 1
            else:
                rated += 1

        return render_template('user_charts.html', 
                                user=user, 
                                to_be_read=to_be_read,
                                have_read=have_read,
                                rated=rated,
                                unrated=unrated,
                                favorites=favorites)
    
    else:
        return redirect("/login")


@app.route('/getnextread')
def get_next_read():
    """Randomly choose the next book a user should read from 'Have Not Read's."""

    next_book_options = []
    user = crud.get_user_by_username(session['user_name'])
    for review in user.reviews:
        if review.to_be_read == True:
            next_book_options.append(review)

    next_book = random.choice(next_book_options)

    return (f'{next_book.book.title} by {next_book.book.author}')


# ----------------------------------------------------------------------------


if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)