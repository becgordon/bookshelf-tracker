from unittest import TestCase
from server import app
from model import connect_to_db, db, example_data
from flask import session
import crud


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

    def test_login(self):
        result = self.client.post("/login",
                                  data={"username": "JackT", "password": "test"},
                                  follow_redirects=True)
        self.assertIn(b"Welcome back, Jack!", result.data)

    def test_get_user_by_username(self):
        user = crud.get_user_by_username('JackT')
        assert('Jack','Torrance','JackT','JackT@test.com','test','/static/images/JackT.jpg') == (user.fname, 
                                                                        user.lname, 
                                                                        user.username,
                                                                        user.email, 
                                                                        user.password,
                                                                        user.profile_image)

    def test_get_all_viewable_users(self):
        user = crud.get_user_by_username('JackT')
        viewable = crud.get_all_viewable_users(user)
        assert('BevM') == viewable[0].username

    def test_get_book_by_isbn(self):
        book = crud.get_book_by_isbn('123')
        assert('If It Bleeds') == book.title

    # def test_sort_books_alphabetically_title(self):
    #     user = crud.get_user_by_username('JackT')
    #     books = crud.sort_books_alphabetically_title(user)
    #     assert('Elevation') == books[0].title
    #     assert('Phantoms') == books[2].title

    def test_does_review_exist(self):
        bool = crud.does_review_exist('1','123')
        assert(bool) == True

    def test_get_review_by_book_and_user_id(self):
        review = crud.get_review_by_book_and_user_id('123','1')
        assert(1) == review.review_id


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


class CRUDTests(TestCase): # all working
    
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