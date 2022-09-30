"""Tests for server.py."""

import server
import unittest

class Testing(unittest.TestCase):

    def test_welcome_page(self):
        client = server.app.test_client()
        result = client.get('/')
        self.assertIn(b'<h1>This is the Welcome Page.</h1>',
                    result.data)

    def test_log_in_page(self):
        client = server.app.test_client()
        result = client.get('/login')
        self.assertIn(b'<form action="/login" method="POST">',
                        result.data)

    def test_log_in(self): # work on the post data on this one
        client = server.app.test_client()
        result = client.post('/login', data={'username':'JackT', 'password':'test'})
        self.assertIn(b'<h1>Welcome back, Jack!</h1>', result.data)

    def test_show_create_account(self):
        client = server.app.test_client()
        result = client.get('/createaccount')
        self.assertIn(b'<form action="/createaccount" method="POST">', 
                        result.data)

if __name__ == '__main__':
    unittest.main()