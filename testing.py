from unittest import TestCase
from server import app
from model import connect_to_db, db, example_data
from flask import session
import crud


class FlaskTestsBasic(TestCase):
    """Flask tests."""

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

    def test_log_out(self):
        with self.client as c:
            with c.session_transaction() as sess:
                sess['user_name'] = 'JackT'

            result = self.client.get('/logout', follow_redirects=True)
            self.assertNotIn(b'user_name', session)
            self.assertIn(b'<h1>This is the Welcome Page.</h1>', result.data)


class FlaskTestsDatabase(TestCase):
    """Flask tests that use the database."""

    def setUp(self):
        self.client = app.test_client()
        app.config['TESTING'] = True
        connect_to_db(app, db_uri="postgresql:///testdb")
        db.create_all()
        example_data()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        db.engine.dispose()

    # def test_login(self): # not working
    #     result = self.client.post("/login",
    #                               data={"username": "JackT", "password": "test"},
    #                               follow_redirects=True)
    #     self.assertIn(b"Welcome back, Jack!", result.data)


class FlaskTestsLoggedIn(TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['SECRET_KEY'] = 'key'
        self.client = app.test_client()
        with self.client as c:
            with c.session_transaction() as sess:
                sess['user_name'] = 'JackT'

    # def test_view_user_profile(self): # not working
    #     result = self.client.get('/userprofile/<username>')
    #     self.assertIn(b'Welcome back, Jack!', result.data)


class CRUDTests(TestCase):

    def test_create_user(self):
        user = crud.create_user('Beverly', 
                                'Marsh', 
                                'BevM@test.com', 
                                'BevM', 
                                'test')
        assert('Beverly', 
                'Marsh',
                'BevM@test.com', 
                'BevM', 
                'test') == (user.fname, 
                            user.lname, 
                            user.email,
                            user.username,
                            user.password)

    def test_create_seed_user(self):
        user = crud.create_seed_user('Beverly', 
                                    'Marsh', 
                                    'BevM@test.com', 
                                    'BevM', 
                                    'test', 
                                    'image')
        assert('Beverly', 
                'Marsh', 
                'BevM', 
                'BevM@test.com', 
                'test', 
                'image') == (user.fname, 
                            user.lname, 
                            user.username,
                            user.email, 
                            user.password,
                            user.profile_image)

    # def test_get_user_by_username(self): # need help here
    #     user = crud.get_user_by_username('JackT')
    #     assert('Jack','Torrance','JackT@test.com','JackT','test') == (user.fname, 
    #                                                                     user.lname, 
    #                                                                     user.username,
    #                                                                     user.email, 
    #                                                                     user.password,
    #                                                                     user.profile_image)

    def test_create_book(self):
        book = crud.create_book('123', 
                                'Carrie', 
                                'Stephen King', 
                                'Sad story.',
                                'Horror', 
                                'image', 
                                '456')
        assert('123', 
                'Carrie', 
                'Stephen King',    
                'Sad story.',
                'Horror', 
                'image', 
                '456') == (book.isbn, 
                            book.title, book.author, 
                            book.description, 
                            book.genre, 
                            book.image, 
                            book.volume_id)

    def test_create_review(self):
        review = crud.create_review('1', '123')
        assert('1','123') == (review.user_id, review.isbn)

    def test_create_seed_review(self):
        review = crud.create_seed_review('1', '123', '3', True, False)
        assert('1', '123', '3', True, False) == (review.user_id, 
                                                    review.isbn, 
                                                    review.score, 
                                                    review.to_be_read, 
                                                    review.favorites)

# ----------------------------------------------------------------------------

if __name__ == "__main__":
    import unittest
    unittest.main()