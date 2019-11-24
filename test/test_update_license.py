#!/usr/bin/env python
import unittest
import os
import json

from updatable import utils as updatable_utils


PATH = os.path.dirname(os.path.realpath(__file__))


def get_pypi_package_data_monkey(package_name, version=None):
    if version:
        json_file = 'pypi-%s-%s.json' % (package_name, version)
    else:
        json_file = 'pypi-%s.json' % package_name

    with open(os.path.join(PATH, 'fixtures', json_file)) as data_file:
        return json.load(data_file)


class TestUpdateLicense(unittest.TestCase):
    """
    Tests package updatability
    """

    def setUp(self):
        self.get_pypi_package_data_orig = updatable_utils.get_pypi_package_data
        updatable_utils.get_pypi_package_data = get_pypi_package_data_monkey

    def tearDown(self):
        updatable_utils.get_pypi_package_data = self.get_pypi_package_data_orig

    def test_update_license(self):
        """
        Test update count for a package that has only major releases
        """
        updates = updatable_utils.get_package_update_list('package3', '1.0.0')
        self.assertEqual(updates['current_release'], '1.0.0')
        self.assertEqual(updates['latest_release'], '3.0.0')
        self.assertEqual(updates['current_release_license'], 'GPL-2.0')
        self.assertEqual(updates['latest_release_license'], 'MIT')

        updates = updatable_utils.get_package_update_list('package3', '2.0.0')
        self.assertEqual(updates['current_release'], '2.0.0')
        self.assertEqual(updates['latest_release'], '3.0.0')
        self.assertEqual(updates['current_release_license'], 'GPL-3.0')
        self.assertEqual(updates['latest_release_license'], 'MIT')

        updates = updatable_utils.get_package_update_list('package3', '3.0.0')
        self.assertEqual(updates['current_release'], '3.0.0')
        self.assertEqual(updates['latest_release'], '3.0.0')
        self.assertEqual(updates['current_release_license'], 'MIT')
        self.assertEqual(updates['latest_release_license'], 'MIT')


if __name__ == '__main__':
    unittest.main()
