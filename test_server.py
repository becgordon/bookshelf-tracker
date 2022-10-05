"""Tests for server.py."""

from server import app
from model import db, connect_to_db, example_data
import unittest


# ----------------------------------------------------------------------------


class FlaskTests(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_welcome_page(self):
        result = self.client.get('/')
        self.assertIn(b'<h1>This is the Welcome Page.</h1>',
                    result.data)

    def test_log_in_page(self):
        result = self.client.get('/login')
        self.assertIn(b'<form action="/login" method="POST">',
                        result.data)

    def test_show_create_account(self):
        result = self.client.get('/createaccount')
        self.assertIn(b'<form action="/createaccount" method="POST">', 
                        result.data)

    # def test_create_account(self): # need to fix this
    #     result = self.client.post('/createaccount', data={'fname':'Jack',
    #                                                     'lname': 'Torrance',
    #                                                     'username':'JackT',
    #                                                     'email':'JackT@test.com',
    #                                                     'password':'test'}, follow_redirects=True)
    #     self.assertIn(b'Account successfully created!', result.data)


class FlaskTestsLoggedIn(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['SECRET_KEY'] = 'key'
        self.client = app.test_client()

        with self.client as c:
            with c.session_transaction() as sess:
                sess['user_name'] = 'JackT'

        connect_to_db(app, db_uri='postgresql://testdb')
        db.create_all()
        example_data()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        db.engine.dispose()

    def test_log_in(self):
        result = self.client.get('/login')
        self.assertIn(b'<a href="/userprofile/JackT">', result.data)

    def test_view_user_profile(self): # not working
        result = self.client.get('/userprofile/JackT')
        self.assertIn(b'Welcome back, Jack!', result.data)

    def test_access_user_settings(self):
        pass

    def test_update_profile_picture(self):
        pass
    
    def test_update_profile_view(self):
        pass

    def test_update_password(self):
        pass

    def test_log_out(self):
        pass

    def test_view_user(self):
        pass

    def test_view_all_users(self):
        pass

    def test_submit_book_search(self):
        pass

    def test_view_advanced_book_search(self):
        pass

    def test_view_book_profile(self):
        pass

    def test_add_book(self):
        pass

    def test_edit_book_settings(self):
        pass

    def test_remove_book(self):
        pass

    def test_sort_books(self):
        pass

    def test_rate_book(self):
        pass

    def test_categorize_book(self):
        pass

    def test_display_shelf(self):
        pass

    def test_view_charts(self):
        pass

    def test_get_next_read(self):
        pass

    def test_set_current_read(self):
        pass


# ----------------------------------------------------------------------------


if __name__ == '__main__':
    unittest.main()