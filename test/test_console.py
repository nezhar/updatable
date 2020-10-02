#!/usr/bin/env python
import sys
import unittest
from unittest.mock import patch
from argparse import ArgumentTypeError
from updatable.console import _str_to_bool, _list_updates, _list_package_updates

try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO


class Capture(list):
    def __enter__(self):
        self._stdout = sys.stdout
        sys.stdout = self._stringio = StringIO()
        return self

    def __exit__(self, *args):
        self.extend(self._stringio.getvalue().splitlines())
        del self._stringio    # free up memory
        sys.stdout = self._stdout


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


class TestListUpdates(unittest.TestCase):

    def test_with_empty_list(self):
        with Capture() as output:
            _list_updates("Test", [], 'MIT')

        self.assertListEqual(output, [])

    def test_with_updates_in_list(self):
        with Capture() as output:
            _list_updates("Test", [
                {"version": "1.0.0", "upload_time": "date 1"},
                {"version": "2.0.0", "upload_time": "date 2"},
            ], 'MIT')

        self.assertListEqual(output, [
            '  Test:',
            '  -- 1.0.0 on date 1 - License: MIT',
            '  -- 2.0.0 on date 2 - License: MIT',
        ])


class TestListPackageUpdates(unittest.TestCase):

    def _mock_get_package_update_list(*args, **kwargs):

        # No updates, no prereeases, no non semantic version
        if args[1] == 'package1':
            return {
                'newer_releases': 0,
                'pre_releases': 0,
                'major_updates': [],
                'minor_updates': [],
                'patch_updates': [],
                'pre_release_updates': [],
                'non_semantic_versions': [],
                'current_release_license': 'MIT',
            }

        # Updates, no prereeases, no non semantic version
        if args[1] == 'package2':
            return {
                'newer_releases': 5,
                'pre_releases': 0,
                'major_updates': [
                    {"version": "2.0.0", "upload_time": "date 3"},
                    {"version": "3.0.0", "upload_time": "date 5"},
                ],
                'minor_updates': [
                    {"version": "1.5.0", "upload_time": "date 2"},
                    {"version": "2.5.0", "upload_time": "date 4"},
                ],
                'patch_updates': [
                    {"version": "1.5.5", "upload_time": "date 5"},
                ],
                'pre_release_updates': [],
                'non_semantic_versions': [],
                'current_release_license': 'MIT',
            }

        # Updates, no prereeases, non semantic version
        if args[1] == 'package3':
            return {
                'newer_releases': 1,
                'pre_releases': 0,
                'major_updates': [
                ],
                'minor_updates': [
                ],
                'patch_updates': [
                    {"version": "1.5.5", "upload_time": "date 5"},
                ],
                'pre_release_updates': [],
                'non_semantic_versions': [
                    {"version": "test1.5.5.3.2.3.23", "upload_time": "date 6"},
                ],
                'current_release_license': 'MIT',
            }

        # Updates, prereeases, non semantic version
        if args[1] == 'package4':
            return {
                'newer_releases': 1,
                'pre_releases': 1,
                'major_updates': [
                ],
                'minor_updates': [
                ],
                'patch_updates': [
                    {"version": "1.5.5", "upload_time": "date 5"},
                ],
                'pre_release_updates': [
                    {"version": "alfa-1.5.5", "upload_time": "date 7"},
                ],
                'non_semantic_versions': [
                    {"version": "test1.5.5.3.2.3.23", "upload_time": "date 6"},
                ],
                'current_release_license': 'MIT',
            }

        # No updates, prereeases, non semantic version
        if args[1] == 'package5':
            return {
                'newer_releases': 0,
                'pre_releases': 1,
                'major_updates': [
                ],
                'minor_updates': [
                ],
                'patch_updates': [],
                'pre_release_updates': [
                    {"version": "alfa-1.5.5", "upload_time": "date 7"},
                ],
                'non_semantic_versions': [
                    {"version": "test1.5.5.3.2.3.23", "upload_time": "date 6"},
                ],
                'current_release_license': 'MIT',
            }

        # Pre releases only
        if args[1] == 'package6':
            return {
                'newer_releases': 0,
                'pre_releases': 1,
                'major_updates': [
                ],
                'minor_updates': [
                ],
                'patch_updates': [],
                'pre_release_updates': [
                    {"version": "alfa-1.5.5", "upload_time": "date 7"},
                ],
                'non_semantic_versions': [],
                'current_release_license': 'MIT',
            }

        # Non semantic version only
        if args[1] == 'package7':
            return {
                'newer_releases': 0,
                'pre_releases': 0,
                'major_updates': [
                ],
                'minor_updates': [
                ],
                'patch_updates': [],
                'pre_release_updates': [],
                'non_semantic_versions': [
                    {"version": "test1.5.5.3.2.3.23", "upload_time": "date 6"},
                ],
                'current_release_license': 'MIT',
            }

    def test_with_no_available_updates(self):
        with patch('updatable.utils.get_package_update_list', side_effect=self._mock_get_package_update_list):
            with Capture() as output:
                _list_package_updates("package1", "1.0.0", False)
            self.assertListEqual(output, [])

            with Capture() as output:
                _list_package_updates("package1", "1.0.0", True)
            self.assertListEqual(output, [])

    def test_with_updates_and_no_prereleases(self):
        with patch('updatable.utils.get_package_update_list', side_effect=self._mock_get_package_update_list):
            with Capture() as output:
                _list_package_updates("package2", "1.0.0", False)
            self.assertListEqual(output, [
                'package2 (1.0.0) - License: MIT',
                '  Major releases:',
                '  -- 2.0.0 on date 3 - License: MIT',
                '  -- 3.0.0 on date 5 - License: MIT',
                '  Minor releases:',
                '  -- 1.5.0 on date 2 - License: MIT',
                '  -- 2.5.0 on date 4 - License: MIT',
                '  Patch releases:',
                '  -- 1.5.5 on date 5 - License: MIT',
                '___'
            ])

            with Capture() as output:
                _list_package_updates("package2", "1.0.0", True)
            self.assertListEqual(output, [
                'package2 (1.0.0) - License: MIT',
                '  Major releases:',
                '  -- 2.0.0 on date 3 - License: MIT',
                '  -- 3.0.0 on date 5 - License: MIT',
                '  Minor releases:',
                '  -- 1.5.0 on date 2 - License: MIT',
                '  -- 2.5.0 on date 4 - License: MIT',
                '  Patch releases:',
                '  -- 1.5.5 on date 5 - License: MIT',
                '___'
            ])

    def test_with_updates_and_no_prereleases_and_non_semantic_versions(self):
        with patch('updatable.utils.get_package_update_list', side_effect=self._mock_get_package_update_list):
            with Capture() as output:
                _list_package_updates("package3", "1.0.0", False)
            self.assertListEqual(output, [
                'package3 (1.0.0) - License: MIT',
                '  Patch releases:',
                '  -- 1.5.5 on date 5 - License: MIT',
                '  Unknown releases:',
                '  -- test1.5.5.3.2.3.23 on date 6 - License: MIT',
                '___'
            ])

            with Capture() as output:
                _list_package_updates("package3", "1.0.0", True)
            self.assertListEqual(output, [
                'package3 (1.0.0) - License: MIT',
                '  Patch releases:',
                '  -- 1.5.5 on date 5 - License: MIT',
                '  Unknown releases:',
                '  -- test1.5.5.3.2.3.23 on date 6 - License: MIT',
                '___'
            ])

    def test_with_updates_and_prereleases_and_non_semantic_versions(self):
        with patch('updatable.utils.get_package_update_list', side_effect=self._mock_get_package_update_list):
            with Capture() as output:
                _list_package_updates("package4", "1.0.0", False)
            self.assertListEqual(output, [
                'package4 (1.0.0) - License: MIT',
                '  Patch releases:',
                '  -- 1.5.5 on date 5 - License: MIT',
                '  Unknown releases:',
                '  -- test1.5.5.3.2.3.23 on date 6 - License: MIT',
                '___'
            ])

            with Capture() as output:
                _list_package_updates("package4", "1.0.0", True)
            self.assertListEqual(output, [
                'package4 (1.0.0) - License: MIT',
                '  Patch releases:',
                '  -- 1.5.5 on date 5 - License: MIT',
                '  Unknown releases:',
                '  -- test1.5.5.3.2.3.23 on date 6 - License: MIT',
                '  Pre releases:',
                '  -- alfa-1.5.5 on date 7 - License: MIT',
                '___'
            ])

    def test_with_prereleases_and_non_semantic_versions(self):
        with patch('updatable.utils.get_package_update_list', side_effect=self._mock_get_package_update_list):
            with Capture() as output:
                _list_package_updates("package5", "1.0.0", False)
            self.assertListEqual(output, [])

            with Capture() as output:
                _list_package_updates("package5", "1.0.0", True)
            self.assertListEqual(output, [
                'package5 (1.0.0) - License: MIT',
                '  Pre releases:',
                '  -- alfa-1.5.5 on date 7 - License: MIT',
                '___'
            ])

    def test_with_prereleases(self):
        with patch('updatable.utils.get_package_update_list', side_effect=self._mock_get_package_update_list):
            with Capture() as output:
                _list_package_updates("package6", "1.0.0", False)
            self.assertListEqual(output, [])

            with Capture() as output:
                _list_package_updates("package6", "1.0.0", True)
            self.assertListEqual(output, [
                'package6 (1.0.0) - License: MIT',
                '  Pre releases:',
                '  -- alfa-1.5.5 on date 7 - License: MIT',
                '___'
            ])

    def test_with_non_semantic_versions(self):
        with patch('updatable.utils.get_package_update_list', side_effect=self._mock_get_package_update_list):
            with Capture() as output:
                _list_package_updates("package7", "1.0.0", False)
            self.assertListEqual(output, [])

            with Capture() as output:
                _list_package_updates("package7", "1.0.0", True)
            self.assertListEqual(output, [])


if __name__ == '__main__':
    unittest.main()
