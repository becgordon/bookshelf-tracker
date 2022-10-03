"""Tests for crud.py."""

import crud
import unittest


# ----------------------------------------------------------------------------


class Testing(unittest.TestCase):
    
    def test_create_user(self):
        self.assertEqual(crud.create_user('Beverly', 'Marsh', 'BevM', 'test'), 
                                            '<User user_id=None name=Beverly Marsh>')

    
    def test_create_seed_user(self):
        pass


    def test_get_user_by_username(self):
        pass


    def test_get_all_viewable_users(self):
        pass


    def test_create_book(self):
        pass


    def test_get_book_by_isbn(self):
        pass


    def test_sort_json_response(self):
        pass


    def test_sort_books_alphabetically_title(self):
        pass


    def test_sort_books_alphabetically_author(self):
        pass


    def test_sort_books_most_recently_added(self):
        pass


    def test_sort_books_least_recently_added(self):
        pass


    def test_create_review(self):
        pass


    def test_create_seed_review(self):
        pass

    def test_does_review_exist(self):
        pass

    def test_get_review_by_book_and_user_id(self):
        pass


# ----------------------------------------------------------------------------


if __name__ == "__main__":
    unittest.main()