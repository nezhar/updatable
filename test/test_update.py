#!/usr/bin/env python
import unittest
from unittest.mock import patch
import os
import json
import datetime

import requests

from updatable import utils as updatable_utils


PATH = os.path.dirname(os.path.realpath(__file__))


def get_pypi_package_data_monkey(package_name, version=None):
    json_file = 'pypi-%s.json' % package_name

    with open(os.path.join(PATH, 'fixtures', json_file)) as data_file:
        return json.load(data_file)


# This method will be used by the mock to replace requests.get
def mocked_pypi_get(*args, **kwargs):
    class MockResponse:

        def __init__(self, json_data, status_code):
            self.ok = True
            self.json_data = json_data
            self.status_code = status_code

        def json(self):
            return self.json_data

    if args[0] == 'https://pypi.org/pypi/updatable/json':
        return MockResponse({"test1": "ok"}, 200)
    elif args[0] == 'https://pypi.org/pypi/updatable/1.0.0/json':
        return MockResponse({"test2": "ok"}, 200)

    return MockResponse(None, 404)


class TestUpdate(unittest.TestCase):
    """
    Tests package updatability
    """

    def setUp(self):
        self.get_pypi_package_data_orig = updatable_utils.get_pypi_package_data
        updatable_utils.get_pypi_package_data = get_pypi_package_data_monkey

    def tearDown(self):
        updatable_utils.get_pypi_package_data = self.get_pypi_package_data_orig

    def test_major_update_count(self):
        """
        Test update count for a package that has only major releases
        """
        updates = updatable_utils.get_package_update_list('package3', '1.0.0')
        self.assertEqual(updates['newer_releases'], 2)
        self.assertEqual(len(updates['major_updates']), 2)
        self.assertEqual(len(updates['minor_updates']), 0)
        self.assertEqual(len(updates['patch_updates']), 0)

        updates = updatable_utils.get_package_update_list('package3', '2.0.0')
        self.assertEqual(updates['newer_releases'], 1)
        self.assertEqual(len(updates['major_updates']), 1)
        self.assertEqual(len(updates['minor_updates']), 0)
        self.assertEqual(len(updates['patch_updates']), 0)

        updates = updatable_utils.get_package_update_list('package3', '3.0.0')
        self.assertEqual(updates['newer_releases'], 0)
        self.assertEqual(len(updates['major_updates']), 0)
        self.assertEqual(len(updates['minor_updates']), 0)
        self.assertEqual(len(updates['patch_updates']), 0)

    def test_major_update_version(self):
        """
        Test update versions for a package that has only major releases.
        This also shows that releases are ordered descendant by release date.
        """
        updates = updatable_utils.get_package_update_list('package3', '1.0.0')
        self.assertEqual(len(updates['major_updates']), 2)
        self.assertEqual(updates['major_updates'][0]['version'], '3.0.0')
        self.assertEqual(updates['major_updates'][1]['version'], '2.0.0')

        updates = updatable_utils.get_package_update_list('package3', '2.0.0')
        self.assertEqual(len(updates['major_updates']), 1)
        self.assertEqual(updates['major_updates'][0]['version'], '3.0.0')

        updates = updatable_utils.get_package_update_list('package3', '3.0.0')
        self.assertEqual(len(updates['major_updates']), 0)

    def test_major_update_date(self):
        """
        Test update upload time for a package that has only major releases.
        This also shows that releases are ordered descendant by release date.
        """
        updates = updatable_utils.get_package_update_list('package3', '1.0.0')
        self.assertEqual(len(updates['major_updates']), 2)
        self.assertEqual(
            updates['major_updates'][0]['upload_time'],
            datetime.datetime(year=2015, month=9, day=29, hour=23, minute=34, second=21)
        )
        self.assertEqual(
            updates['major_updates'][1]['upload_time'],
            datetime.datetime(year=2013, month=11, day=29, hour=23, minute=34, second=21)
        )

        updates = updatable_utils.get_package_update_list('package3', '2.0.0')
        self.assertEqual(len(updates['major_updates']), 1)
        self.assertEqual(
            updates['major_updates'][0]['upload_time'],
            datetime.datetime(year=2015, month=9, day=29, hour=23, minute=34, second=21)
        )

        updates = updatable_utils.get_package_update_list('package3', '3.0.0')
        self.assertEqual(len(updates['major_updates']), 0)

    def test_minor_update_count(self):
        """
        Test update count for a package that has only minor releases
        """
        updates = updatable_utils.get_package_update_list('package2', '1.0.0')
        self.assertEqual(updates['newer_releases'], 3)
        self.assertEqual(len(updates['major_updates']), 0)
        self.assertEqual(len(updates['minor_updates']), 3)
        self.assertEqual(len(updates['patch_updates']), 0)

        updates = updatable_utils.get_package_update_list('package2', '1.1.0')
        self.assertEqual(updates['newer_releases'], 2)
        self.assertEqual(len(updates['major_updates']), 0)
        self.assertEqual(len(updates['minor_updates']), 2)
        self.assertEqual(len(updates['patch_updates']), 0)

        updates = updatable_utils.get_package_update_list('package2', '1.2.0')
        self.assertEqual(updates['newer_releases'], 1)
        self.assertEqual(len(updates['major_updates']), 0)
        self.assertEqual(len(updates['minor_updates']), 1)
        self.assertEqual(len(updates['patch_updates']), 0)

        updates = updatable_utils.get_package_update_list('package2', '1.3.0')
        self.assertEqual(updates['newer_releases'], 0)
        self.assertEqual(len(updates['major_updates']), 0)
        self.assertEqual(len(updates['minor_updates']), 0)
        self.assertEqual(len(updates['patch_updates']), 0)

    def test_minor_update_version(self):
        """
        Test update versions for a package that has only minor releases.
        This also shows that releases are ordered descendant by release date.
        """
        updates = updatable_utils.get_package_update_list('package2', '1.0.0')
        self.assertEqual(len(updates['minor_updates']), 3)
        self.assertEqual(updates['minor_updates'][0]['version'], '1.3.0')
        self.assertEqual(updates['minor_updates'][1]['version'], '1.2.0')
        self.assertEqual(updates['minor_updates'][2]['version'], '1.1.0')

        updates = updatable_utils.get_package_update_list('package2', '1.1.0')
        self.assertEqual(len(updates['minor_updates']), 2)
        self.assertEqual(updates['minor_updates'][0]['version'], '1.3.0')
        self.assertEqual(updates['minor_updates'][1]['version'], '1.2.0')

        updates = updatable_utils.get_package_update_list('package2', '1.2.0')
        self.assertEqual(len(updates['minor_updates']), 1)
        self.assertEqual(updates['minor_updates'][0]['version'], '1.3.0')

        updates = updatable_utils.get_package_update_list('package2', '1.3.0')
        self.assertEqual(len(updates['minor_updates']), 0)

    def test_minor_update_date(self):
        """
        Test update upload time for a package that has only minor releases.
        This also shows that releases are ordered descendant by release date.
        """
        updates = updatable_utils.get_package_update_list('package2', '1.0.0')
        self.assertEqual(len(updates['minor_updates']), 3)
        self.assertEqual(
            updates['minor_updates'][0]['upload_time'],
            datetime.datetime(year=2015, month=9, day=29, hour=23, minute=34, second=21)
        )
        self.assertEqual(
            updates['minor_updates'][1]['upload_time'],
            datetime.datetime(year=2014, month=9, day=29, hour=23, minute=34, second=21)
        )
        self.assertEqual(
            updates['minor_updates'][2]['upload_time'],
            datetime.datetime(year=2013, month=10, day=29, hour=23, minute=34, second=21)
        )

        updates = updatable_utils.get_package_update_list('package2', '1.1.0')
        self.assertEqual(len(updates['minor_updates']), 2)
        self.assertEqual(
            updates['minor_updates'][0]['upload_time'],
            datetime.datetime(year=2015, month=9, day=29, hour=23, minute=34, second=21)
        )
        self.assertEqual(
            updates['minor_updates'][1]['upload_time'],
            datetime.datetime(year=2014, month=9, day=29, hour=23, minute=34, second=21)
        )

        updates = updatable_utils.get_package_update_list('package2', '1.2.0')
        self.assertEqual(len(updates['minor_updates']), 1)
        self.assertEqual(
            updates['minor_updates'][0]['upload_time'],
            datetime.datetime(year=2015, month=9, day=29, hour=23, minute=34, second=21)
        )

        updates = updatable_utils.get_package_update_list('package2', '1.3.0')
        self.assertEqual(len(updates['minor_updates']), 0)

    def test_patch_update_count(self):
        """
        Test update count for a package that has only patch releases
        """
        updates = updatable_utils.get_package_update_list('package1', '1.0.0')
        self.assertEqual(updates['newer_releases'], 2)
        self.assertEqual(len(updates['major_updates']), 0)
        self.assertEqual(len(updates['minor_updates']), 0)
        self.assertEqual(len(updates['patch_updates']), 2)

        updates = updatable_utils.get_package_update_list('package1', '1.0.1')
        self.assertEqual(updates['newer_releases'], 1)
        self.assertEqual(len(updates['major_updates']), 0)
        self.assertEqual(len(updates['minor_updates']), 0)
        self.assertEqual(len(updates['patch_updates']), 1)

        updates = updatable_utils.get_package_update_list('package1', '1.0.2')
        self.assertEqual(updates['newer_releases'], 0)
        self.assertEqual(len(updates['major_updates']), 0)
        self.assertEqual(len(updates['minor_updates']), 0)
        self.assertEqual(len(updates['patch_updates']), 0)

    def test_patch_update_version(self):
        """
        Test update versions for a package that has only patch releases.
        This also shows that releases are ordered descendant by release date.
        """
        updates = updatable_utils.get_package_update_list('package1', '1.0.0')
        self.assertEqual(len(updates['patch_updates']), 2)
        self.assertEqual(updates['patch_updates'][0]['version'], '1.0.2')
        self.assertEqual(updates['patch_updates'][1]['version'], '1.0.1')

        updates = updatable_utils.get_package_update_list('package1', '1.0.1')
        self.assertEqual(len(updates['patch_updates']), 1)
        self.assertEqual(updates['patch_updates'][0]['version'], '1.0.2')

        updates = updatable_utils.get_package_update_list('package1', '1.0.2')
        self.assertEqual(len(updates['patch_updates']), 0)

    def test_patch_update_date(self):
        """
        Test update upload time for a package that has only patch releases.
        This also shows that releases are ordered descendant by release date.
        """
        updates = updatable_utils.get_package_update_list('package1', '1.0.0')
        self.assertEqual(len(updates['patch_updates']), 2)
        self.assertEqual(
            updates['patch_updates'][0]['upload_time'],
            datetime.datetime(year=2013, month=10, day=22, hour=23, minute=34, second=21)
        )
        self.assertEqual(
            updates['patch_updates'][1]['upload_time'],
            datetime.datetime(year=2013, month=9, day=29, hour=23, minute=34, second=21)
        )

        updates = updatable_utils.get_package_update_list('package1', '1.0.1')
        self.assertEqual(len(updates['patch_updates']), 1)
        self.assertEqual(
            updates['patch_updates'][0]['upload_time'],
            datetime.datetime(year=2013, month=10, day=22, hour=23, minute=34, second=21)
        )

        updates = updatable_utils.get_package_update_list('package1', '1.0.2')
        self.assertEqual(len(updates['patch_updates']), 0)

    def test_unusual_semantic_count(self):
        """
        Test for packages for a package with unusual versions
        """
        updates = updatable_utils.get_package_update_list('package5', '0.9999999')
        self.assertEqual(updates['newer_releases'], 2)
        self.assertEqual(len(updates['major_updates']), 0)
        self.assertEqual(len(updates['minor_updates']), 2)
        self.assertEqual(len(updates['patch_updates']), 0)

        updates = updatable_utils.get_package_update_list('package5', '0.99999999')
        self.assertEqual(updates['newer_releases'], 1)
        self.assertEqual(len(updates['major_updates']), 0)
        self.assertEqual(len(updates['minor_updates']), 1)
        self.assertEqual(len(updates['patch_updates']), 0)

        updates = updatable_utils.get_package_update_list('package5', '0.999999999')
        self.assertEqual(updates['newer_releases'], 0)
        self.assertEqual(len(updates['major_updates']), 0)
        self.assertEqual(len(updates['minor_updates']), 0)
        self.assertEqual(len(updates['patch_updates']), 0)

    def test_non_semantic_count(self):
        """
        Test for package with non semantic verions
        """
        updates = updatable_utils.get_package_update_list('package6', '0.1')
        self.assertEqual(updates['newer_releases'], 0)
        self.assertEqual(len(updates['major_updates']), 0)
        self.assertEqual(len(updates['minor_updates']), 0)
        self.assertEqual(len(updates['patch_updates']), 0)
        self.assertEqual(len(updates['non_semantic_versions']), 3)


class TestGetPackageData(unittest.TestCase):

    @patch('requests.get', side_effect=mocked_pypi_get)
    def test_get_pypi_package_data_no_version(self, mock):
        """
        Assures that fetched pypi data is parsed correctly if no version is given
        """
        response = updatable_utils.get_pypi_package_data('updatable')
        self.assertTrue(mock.called)
        self.assertDictEqual(response, {"test1": "ok"})

    @patch('requests.get', side_effect=mocked_pypi_get)
    def test_get_pypi_package_data_existing_version(self, mock):
        """
        Assures that fetched pypi data is parsed correctly if a valid version is given
        """
        response = updatable_utils.get_pypi_package_data('updatable', '1.0.0')
        self.assertTrue(mock.called)
        self.assertDictEqual(response, {"test2": "ok"})

    @patch('requests.get', side_effect=mocked_pypi_get)
    def test_get_pypi_package_data_with_non_existing_version(self, mock):
        """
        Assures that None is return if a invalid version is given
        """
        response = updatable_utils.get_pypi_package_data('updatable', '2.0.0')
        self.assertTrue(mock.called)
        self.assertEqual(response, None)

    @patch('requests.get', side_effect=requests.ConnectionError)
    def test_get_pypi_package_data_with_connection_error(self, mock):
        """
        Assures a RuntimeError is raised on connection error
        """
        with self.assertRaises(RuntimeError):
            updatable_utils.get_pypi_package_data('updatable')

        self.assertTrue(mock.called)


if __name__ == '__main__':
    unittest.main()
