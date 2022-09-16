"""Server for bookshelf tracking app."""

from flask import Flask, render_template, request, flash, session, redirect
import os
from model import connect_to_db, db, Book
import requests
import crud

from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = "dev"

BOOKS_API_KEY = os.environ['GOOGLE_BOOKS_KEY']

app.jinja_env.undefined = StrictUndefined


@app.route('/')
def welcome_page():
    """View welcome page."""
    
    return render_template('welcome_page.html')


@app.route('/findbookstore')
def find_bookstore():
    """Find bookstores based on location."""
    pass


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

    if user and 'user_name' in session and session['user_name'] == username:
        return render_template('user_profile.html', user=user)
    else:
        return redirect("/login")


@app.route('/logout') # HELP HERE
def log_out():
    """Allow a user to log out."""
    session.clear()
    
    return redirect('/')


@app.route('/booksearch')
def search_books():
    """Displays book search page."""
    return render_template('book_search.html')


@app.route('/booksearch/<searchterm>')
def submit_book_search(searchterm):
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

    #     isbn = data['items'][n]['volumeInfo']['industryIdentifiers'][0]['identifier']
    #     title = data['items'][n]['volumeInfo']['title']
    #     author = str(data['items'][n]['volumeInfo']['authors'])
    #     description = data['items'][n]['volumeInfo']['description']
    #     genre = str(data['items'][n]['volumeInfo']['categories'])
    #     image = data['items'][n]['volumeInfo']['imageLinks']['thumbnail']

    
    return render_template('book_search_results.html',books=books, searchterm=searchterm)


@app.route('/bookprofile/<volume_id>')
def view_book_profile(volume_id):
    """View a particular book's profile."""
    
    url = f'https://www.googleapis.com/books/v1/volumes/{volume_id}'
    payload = {'apikey': BOOKS_API_KEY}
    print(url)
    res = requests.get(url, params=payload)
    profile = res.json()
    print(profile)
    return render_template('book_profile.html', profile=profile)


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
        if 'categories' in book['volumeInfo']:
            genre = ' '.join(book['volumeInfo']['categories'])
        else:
            genre = None
        image = book['volumeInfo']['imageLinks']['thumbnail']
        
        book = crud.create_book(isbn, title, author, description, genre, image)

        db.session.add(book)

    score = None
    user = crud.get_user_by_username(session['user_name'])
    review = crud.create_review(score, user.user_id, isbn)

    db.session.add(review)
    db.session.commit()
        
    return redirect(f'/userprofile/{user.username}')


if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)