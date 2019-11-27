#!/usr/bin/env python
import unittest
from argparse import ArgumentTypeError
from updatable.console import _str_to_bool


class TestStrToBool(unittest.TestCase):

    def test_str_to_bool_true(self):
        self.assertTrue(_str_to_bool(True))
        self.assertTrue(_str_to_bool('t'))
        self.assertTrue(_str_to_bool('y'))
        self.assertTrue(_str_to_bool('True'))
        self.assertTrue(_str_to_bool('YES'))
        self.assertTrue(_str_to_bool('1'))

    def test_str_to_bool_false(self):
        self.assertFalse(_str_to_bool(False))
        self.assertFalse(_str_to_bool('f'))
        self.assertFalse(_str_to_bool('n'))
        self.assertFalse(_str_to_bool('False'))
        self.assertFalse(_str_to_bool('NO'))
        self.assertFalse(_str_to_bool('0'))

    def test_str_to_bool_exception(self):
        with self.assertRaises(ArgumentTypeError):
            _str_to_bool('')

        with self.assertRaises(ArgumentTypeError):
            _str_to_bool('falsy')

        with self.assertRaises(ArgumentTypeError):
            _str_to_bool('eye')


if __name__ == '__main__':
    unittest.main()
