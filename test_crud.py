"""Tests for crud.py."""

import crud
import unittest

class Testing(unittest.TestCase):
    
    def test_create_user(self):
        self.assertEqual(crud.create_user('Beverly', 'Marsh', 'BevM', 'test'), 
                                            '<User user_id=None name=Beverly Marsh>')


if __name__ == "__main__":
    unittest.main()