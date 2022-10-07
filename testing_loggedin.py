from unittest import TestCase
from server import app
from model import connect_to_db, db, example_data
from flask import session
import crud

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

