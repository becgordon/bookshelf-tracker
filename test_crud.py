"""Tests for crud.py."""

import crud
import unittest


# ----------------------------------------------------------------------------


class Testing(unittest.TestCase):
    
    def test_create_user(self):
        user = crud.create_user('Beverly', 'Marsh', 'BevM', 'test')
        assert('Beverly', 'Marsh', 'BevM', 'test') == (user.fname, 
                                                        user.lname, 
                                                        user.username, 
                                                        user.password)

    def test_create_seed_user(self):
        user = crud.create_seed_user('Beverly', 'Marsh', 'BevM', 'test', 'image')
        assert('Beverly', 'Marsh', 'BevM', 'test', 'image') == (user.fname, 
                                                        user.lname, 
                                                        user.username, 
                                                        user.password,
                                                        user.profile_image)

    def test_get_user_by_username(self):
        pass

    def test_get_all_viewable_users(self):
        pass

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
        review = crud.create_review('1', '123')
        assert('1','123') == (review.user_id, review.isbn)

    def test_create_seed_review(self):
        review = crud.create_seed_review('1', '123', '3', True, False)
        assert('1', '123', '3', True, False) == (review.user_id, 
                                                    review.isbn, 
                                                    review.score, 
                                                    review.to_be_read, 
                                                    review.favorites)

    def test_does_review_exist(self):
        pass

    def test_get_review_by_book_and_user_id(self):
        pass


# ----------------------------------------------------------------------------


if __name__ == "__main__":
    unittest.main()