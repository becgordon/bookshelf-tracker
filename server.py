"""Server for bookshelf tracking app."""

from flask import Flask, render_template, request, flash, session, redirect
import os
import random
import cloudinary.uploader
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from password_generator import PasswordGenerator

from model import connect_to_db, db
import requests
import crud

from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = "dev"

BOOKS_API_KEY = os.environ['GOOGLE_BOOKS_KEY']
CLOUDINARY_KEY = os.environ['CLOUDINARY_KEY']
CLOUDINARY_SECRET = os.environ['CLOUDINARY_SECRET']
CLOUD_NAME = 'ddcfjqpxh'
SENDGRID_API_KEY = os.environ['SENDGRID_API_KEY']
PWO = PasswordGenerator()

app.jinja_env.undefined = StrictUndefined


#  BASIC ROUTES --------------------------------------------------------------


@app.route('/')
def welcome_page():
    """View welcome page."""

    if session:
        username = session.get("user_name")
        return redirect(f'/userprofile/{username}')
    else:
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
        return render_template('login.html')
    else:
        session['user_name'] = user.username
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
    email = request.form.get('email')
    username = request.form.get('username')
    password = request.form.get('password')
    confirm_password = request.form.get('confirm-password')

    user = crud.get_user_by_username(username)

    if user:
        flash("Sorry! That username is already taken.")
        return render_template('create_account.html')
    elif password != confirm_password:
        flash("Your passwords don't match.")
        return render_template('create_account.html')
    else:
        user = crud.create_user(fname, lname, email, username, password)
        db.session.add(user)
        db.session.commit()
        flash('Account creation successful!')

    return render_template('login.html')


@app.route('/userprofile/<username>')
def view_user_profile(username):
    """View a particular user's profile."""

    user = crud.get_user_by_username(username)
    current_reads = []
    for review in user.reviews:
        if review.current_read == True:
            current_reads.append(review)

    if user and 'user_name' in session and session['user_name'] == username:
        return render_template('user_profile.html', user=user, current_reads=current_reads)
    else:
        return redirect("/login")


@app.route('/usersettings/<username>')
def access_user_settings(username):
    """Access the user's settings."""

    user = crud.get_user_by_username(username)

    if user and 'user_name' in session and session['user_name'] == username:
        return render_template('user_settings.html', user=user)
    else:
        return redirect("/login")


@app.route('/updateprofile/<username>', methods=['POST'])
def update_profile_picture(username):
    """Update a user's profile picture."""

    user = crud.get_user_by_username(username)

    if user and 'user_name' in session and session['user_name'] == username:
        file = request.files['profile-picture']
        profile_picture = cloudinary.uploader.upload(file,
                                            api_key=CLOUDINARY_KEY,
                                            api_secret=CLOUDINARY_SECRET,
                                            cloud_name=CLOUD_NAME)
        saved_profile_picture = profile_picture['secure_url']
        user.profile_image = saved_profile_picture
        db.session.commit()
        return redirect(f'/userprofile/{user.username}')
    else:
        return redirect("/login")


@app.route('/updateprofileview')
def update_profile_view():
    """Update whether a user's library can be view by others."""

    user = crud.get_user_by_username(session['user_name'])
    if user.profile_view == True:
        view = False
    else:
        view = True
    user.profile_view = view
    db.session.commit()

    return render_template('user_settings.html', user=user)


@app.route('/updatepassword/<username>')
def update_password(username):
    """Update a user's password."""
    
    user = crud.get_user_by_username(username)

    if user and 'user_name' in session and session['user_name'] == username:
        current_password = request.args.get('current-password')
        new_password = request.args.get('new-password')
        confirm_new_password = request.args.get('confirm-new-password')

        if current_password == user.password and new_password == confirm_new_password:
            user.password = new_password
            db.session.commit()
            flash('Your password was updated successfully.')
            return redirect(f'/userprofile/{user.username}')
        else:
            flash("Either your current password is not correct or you new passwords don't match. Please try again.")
            return render_template('user_settings.html', user=user)


@app.route('/logout') 
def log_out():
    """Allow a user to log out."""
    session.clear()
    
    return redirect('/')


@app.route('/userlibrary/<username>')
def view_user(username):
    """View another user's library."""

    viewed_user = crud.get_user_by_username(username)
    current_reads = []
    for review in viewed_user.reviews:
        if review.current_read == True:
            current_reads.append(review)

    return render_template('user_library.html', 
                            viewed_user=viewed_user, 
                            current_reads=current_reads)


@app.route('/resetpassword')
def show_reset_password():
    """Show form to reset a user's password."""

    return render_template('password_reset.html')

@app.route('/resetpassword', methods=['POST'])
def submit_reset_password():
    """Reset a user's password."""

    reset_id = PWO.generate()
    reset_email = request.form.get('reset-email')
    reset_password = crud.create_password_reset(reset_id, reset_email)
    db.session.add(reset_password)
    db.session.commit()

    message = Mail(
        from_email='shelfhelplibrarytracker@gmail.com',
        to_emails=f'{reset_email}',
        subject='Shelf-Help: Requested Password Reset',
        html_content=f'<h1>Hello! You can reset your password by following this link: localhost:5000/resetpassword/{reset_id}<h1/>')
    try:
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        sg.send(message)
    except Exception:
        print("ERROR: PC LOAD LETTER")

    return render_template('password_reset_submit.html')


@app.route('/resetpassword/<reset_id>')
def password_reset_link(reset_id):
    """Password reset link leads here."""

    reset = crud.get_reset_by_reset_id(reset_id)

    return render_template('password_rest_link.html', 
                            email=reset.email, 
                            reset_id=reset_id)


@app.route('/resetpassword/<reset_id>', methods=['POST'])
def password_change(reset_id):
    """Password reset link leads here."""

    reset = crud.get_reset_by_reset_id(reset_id)
    reset_password = request.form.get('reset-password')
    user = crud.get_user_by_email(reset.email)
    user.password = reset_password
    db.session.commit()
    flash('Password reset successful!')

    return render_template('login.html')


@app.route('/deleteaccount')
def show_delete_account():
    """Show form for user to delete their account."""

    return render_template('delete_account.html')


@app.route('/deleteaccount', methods=['POST'])
def submit_delete_account():
    """Delete a user's account."""
    
    user = crud.get_user_by_username(session['user_name'])
    password = request.form.get('password')
    confirm_password = request.form.get('confirm-password')

    if password == user.password and confirm_password == user.password:
        for review in user.reviews:
            db.session.delete(review)
        db.session.delete(user)
        db.session.commit()
    else:
        flash("You've either entered the wrong password or they don't match.")
        return render_template('delete_account.html')
    flash("Account deleted successfully!")

    return render_template('login.html')


# BOOK ROUTES ----------------------------------------------------------------


@app.route('/viewallusers')
def view_all_users():
    """View all users on platform."""

    user = crud.get_user_by_username(session['user_name'])
    users = crud.get_all_viewable_users(user)

    return render_template('all_users.html', users=users)


@app.route('/booksearchresults')
def submit_book_search():
    """Takes in search term an returns results that match."""

    search_term = request.args.get('search-term')
    advanced_search_term = request.args.get('advanced-search-term')
    search_type = request.args.get('search-type')

    url = 'https://www.googleapis.com/books/v1/volumes'
    payload = {'apikey': BOOKS_API_KEY, 
                'q': search_term, 
                f'{search_type}': advanced_search_term}

    response = (requests.get(url, params=payload)).json()

    if 'items' in response:
        books = response['items']
    else:
        books = []
    
    return render_template('book_search_results.html',
                            books=books, 
                            searchterm=search_term)


@app.route('/advancedbooksearch')
def view_advanced_book_search():
    """View advanced book search page."""

    return render_template('advanced_book_search.html')


@app.route('/bookprofile/<volume_id>')
def view_book_profile(volume_id):
    """View a particular book's profile."""
    
    url = f'https://www.googleapis.com/books/v1/volumes/{volume_id}'
    payload = {'apikey': BOOKS_API_KEY}
    response = (requests.get(url, params=payload)).json()

    (title, 
    author, 
    image, 
    genre, 
    isbn, 
    description, 
    volume_id) = crud.sort_json_response(response)

    return render_template('book_profile.html',
                            title=title,
                            author=author,
                            image=image,
                            genre=genre,
                            isbn=isbn,
                            volume_id=volume_id,
                            description=description)


@app.route('/addbook/<volume_id>')
def add_book(volume_id):
    """Adds a book to a particular user's library."""

    url = f'https://www.googleapis.com/books/v1/volumes/{volume_id}'
    payload = {'apikey': BOOKS_API_KEY}

    response = (requests.get(url, params=payload)).json()

    (title, 
    author, 
    image, 
    genre, 
    isbn, 
    description, 
    volume_id) = crud.sort_json_response(response)
   
    if not crud.get_book_by_isbn(isbn):
        book = crud.create_book(isbn, title, author, description, genre, image, volume_id)
        db.session.add(book)

    user = crud.get_user_by_username(session['user_name'])

    if not crud.does_review_exist(user.user_id, isbn):
        review = crud.create_review(user.user_id, isbn)
        db.session.add(review)
        db.session.commit()
    else:
        flash("You've already added this book.") # not currently flashing message
        
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

    current_reads = []
    for review in user.reviews:
        if review.current_read == True:
            current_reads.append(review)

    return render_template('user_profile.html', 
                            user=user, 
                            current_reads=current_reads)


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

    return next_book.book.image


@app.route('/currentread/<isbn>')
def set_current_read(isbn):
    """Set a book as current read."""

    user = crud.get_user_by_username(session['user_name'])
    review = crud.get_review_by_book_and_user_id(isbn, user.user_id)
    if review.current_read == False:
        review.current_read = True
    else: 
        review.current_read = False
    db.session.commit()

    return redirect(f'/userprofile/{user.username}')


# ----------------------------------------------------------------------------


if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)