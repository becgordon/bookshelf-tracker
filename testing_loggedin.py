from unittest import TestCase
from server import app
from model import connect_to_db, db, example_data
from flask import session

class FlaskTestsLoggedInDatabase(TestCase):
    """Flask tests that use the database."""

    def setUp(self):
        self.client = app.test_client()
        app.config['TESTING'] = True
        connect_to_db(app, db_uri="postgresql:///loggedintestdb")
        db.create_all()
        example_data()
        with self.client as c:
            with c.session_transaction() as sess:
                sess['user_name'] = 'JackT'

    def tearDown(self):
        with self.client as c:
            with c.session_transaction() as sess:
                sess.clear()
        db.session.remove()
        db.drop_all()
        db.engine.dispose()

    def test_view_user_profile(self):
        result = self.client.get('/userprofile/JackT')
        self.assertIn(b'Welcome back, Jack!', result.data)

    def test_access_user_settings(self):
        result = self.client.get('/usersettings/JackT')
        self.assertIn(b'<h3>Update your password.</h3>', result.data)

    def test_log_out(self):
        result = self.client.get('/logout', follow_redirects=True)
        self.assertIn(b'<title>Welcome Page</title>', result.data)

    def test_view_user(self):
        result = self.client.get('/userlibrary/BevM')
        self.assertIn(b"BevM's Library", result.data)

    def test_view_all_users(self):
        result = self.client.get('/viewallusers')
        self.assertIn(b'<title>View all users</title>', result.data)

    def test_submit_book_search(self):
        result = self.client.get('/booksearchresults', data={'search_term':'Stephen King'})
        self.assertIn(b'Showing results for', result.data)

    def test_view_book_profile(self):
        result = self.client.get('/bookprofile/Fb5nAwAAQBAJ')
        self.assertIn(b'9781408176634', result.data)