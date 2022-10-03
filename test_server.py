"""Tests for server.py."""

import server
import unittest


# ----------------------------------------------------------------------------


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
        pass

    def test_show_create_account(self):
        client = server.app.test_client()
        result = client.get('/createaccount')
        self.assertIn(b'<form action="/createaccount" method="POST">', 
                        result.data)

    def test_create_account(self):
        pass

    def test_view_user_profile(self):
        pass

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