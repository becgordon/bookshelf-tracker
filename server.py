"""Server for bookshelf tracking app."""

from flask import Flask, render_template, request, flash, session, redirect
from model import connect_to_db, db 
import crud

from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = "dev"
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
    return render_template('login.html')


@app.route('/login', methods=["POST"])
def log_in():
    """Submits log in info and goes to user profile."""
    
    username = request.form.get('username')
    password = request.form.get('password')

    user = crud.get_user_by_username(username)

    if not user or user.password != password:
        flash("The email or password entered were incorrect.")
    else:
        session['user_name'] = user.username
        flash("Successfully logged in!")
    
    return redirect('/userprofile/<username>')


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

    return render_template('user_profile.html', user=user)


@app.route('/booksearch?searchterm=<searchterm>')
def search_books():
    """Search for books matching a particular term."""
    pass


@app.route('/bookprofile?book={book.isbn}')
def view_book_profile():
    """View a particular book's profile."""
    pass


if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)