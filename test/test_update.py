#!/usr/bin/env python
import unittest
import os
import json
import datetime

import updatable


PATH = os.path.dirname(os.path.realpath(__file__))


def get_pypi_package_data_monkey(package_name, version=None):
    json_file = 'pypi-%s.json' % package_name

    with open(os.path.join(PATH, 'fixtures', json_file)) as data_file:
        return json.load(data_file)


class TestUpdate(unittest.TestCase):
    """
    Tests package updatability
    """

    def setUp(self):
        self.get_pypi_package_data_orig = updatable.get_pypi_package_data
        updatable.get_pypi_package_data = get_pypi_package_data_monkey

    def tearDown(self):
        updatable.get_pypi_package_data = self.get_pypi_package_data_orig

    def test_major_update_count(self):
        """
        Test update count for a package that has only major releases
        """
        updates = updatable.get_package_update_list('package3', '1.0.0')
        self.assertEqual(updates['newer_releases'], 2)
        self.assertEqual(len(updates['major_updates']), 2)
        self.assertEqual(len(updates['minor_updates']), 0)
        self.assertEqual(len(updates['patch_updates']), 0)

        updates = updatable.get_package_update_list('package3', '2.0.0')
        self.assertEqual(updates['newer_releases'], 1)
        self.assertEqual(len(updates['major_updates']), 1)
        self.assertEqual(len(updates['minor_updates']), 0)
        self.assertEqual(len(updates['patch_updates']), 0)

        updates = updatable.get_package_update_list('package3', '3.0.0')
        self.assertEqual(updates['newer_releases'], 0)
        self.assertEqual(len(updates['major_updates']), 0)
        self.assertEqual(len(updates['minor_updates']), 0)
        self.assertEqual(len(updates['patch_updates']), 0)

    def test_major_update_version(self):
        """
        Test update versions for a package that has only major releases.
        This also shows that releases are ordered descendant by release date.
        """
        updates = updatable.get_package_update_list('package3', '1.0.0')
        self.assertEqual(len(updates['major_updates']), 2)
        self.assertEqual(updates['major_updates'][0]['version'], '3.0.0')
        self.assertEqual(updates['major_updates'][1]['version'], '2.0.0')

        updates = updatable.get_package_update_list('package3', '2.0.0')
        self.assertEqual(len(updates['major_updates']), 1)
        self.assertEqual(updates['major_updates'][0]['version'], '3.0.0')

        updates = updatable.get_package_update_list('package3', '3.0.0')
        self.assertEqual(len(updates['major_updates']), 0)

    def test_major_update_date(self):
        """
        Test update upload time for a package that has only major releases.
        This also shows that releases are ordered descendant by release date.
        """
        updates = updatable.get_package_update_list('package3', '1.0.0')
        self.assertEqual(len(updates['major_updates']), 2)
        self.assertEqual(
            updates['major_updates'][0]['upload_time'],
            datetime.datetime(year=2015, month=9, day=29, hour=23, minute=34, second=21)
        )
        self.assertEqual(
            updates['major_updates'][1]['upload_time'],
            datetime.datetime(year=2013, month=11, day=29, hour=23, minute=34, second=21)
        )

        updates = updatable.get_package_update_list('package3', '2.0.0')
        self.assertEqual(len(updates['major_updates']), 1)
        self.assertEqual(
            updates['major_updates'][0]['upload_time'],
            datetime.datetime(year=2015, month=9, day=29, hour=23, minute=34, second=21)
        )

        updates = updatable.get_package_update_list('package3', '3.0.0')
        self.assertEqual(len(updates['major_updates']), 0)

    def test_minor_update_count(self):
        """
        Test update count for a package that has only minor releases
        """
        updates = updatable.get_package_update_list('package2', '1.0.0')
        self.assertEqual(updates['newer_releases'], 3)
        self.assertEqual(len(updates['major_updates']), 0)
        self.assertEqual(len(updates['minor_updates']), 3)
        self.assertEqual(len(updates['patch_updates']), 0)

        updates = updatable.get_package_update_list('package2', '1.1.0')
        self.assertEqual(updates['newer_releases'], 2)
        self.assertEqual(len(updates['major_updates']), 0)
        self.assertEqual(len(updates['minor_updates']), 2)
        self.assertEqual(len(updates['patch_updates']), 0)

        updates = updatable.get_package_update_list('package2', '1.2.0')
        self.assertEqual(updates['newer_releases'], 1)
        self.assertEqual(len(updates['major_updates']), 0)
        self.assertEqual(len(updates['minor_updates']), 1)
        self.assertEqual(len(updates['patch_updates']), 0)

        updates = updatable.get_package_update_list('package2', '1.3.0')
        self.assertEqual(updates['newer_releases'], 0)
        self.assertEqual(len(updates['major_updates']), 0)
        self.assertEqual(len(updates['minor_updates']), 0)
        self.assertEqual(len(updates['patch_updates']), 0)

    def test_minor_update_version(self):
        """
        Test update versions for a package that has only minor releases.
        This also shows that releases are ordered descendant by release date.
        """
        updates = updatable.get_package_update_list('package2', '1.0.0')
        self.assertEqual(len(updates['minor_updates']), 3)
        self.assertEqual(updates['minor_updates'][0]['version'], '1.3.0')
        self.assertEqual(updates['minor_updates'][1]['version'], '1.2.0')
        self.assertEqual(updates['minor_updates'][2]['version'], '1.1.0')

        updates = updatable.get_package_update_list('package2', '1.1.0')
        self.assertEqual(len(updates['minor_updates']), 2)
        self.assertEqual(updates['minor_updates'][0]['version'], '1.3.0')
        self.assertEqual(updates['minor_updates'][1]['version'], '1.2.0')

        updates = updatable.get_package_update_list('package2', '1.2.0')
        self.assertEqual(len(updates['minor_updates']), 1)
        self.assertEqual(updates['minor_updates'][0]['version'], '1.3.0')

        updates = updatable.get_package_update_list('package2', '1.3.0')
        self.assertEqual(len(updates['minor_updates']), 0)

    def test_minor_update_date(self):
        """
        Test update upload time for a package that has only minor releases.
        This also shows that releases are ordered descendant by release date.
        """
        updates = updatable.get_package_update_list('package2', '1.0.0')
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

        updates = updatable.get_package_update_list('package2', '1.1.0')
        self.assertEqual(len(updates['minor_updates']), 2)
        self.assertEqual(
            updates['minor_updates'][0]['upload_time'],
            datetime.datetime(year=2015, month=9, day=29, hour=23, minute=34, second=21)
        )
        self.assertEqual(
            updates['minor_updates'][1]['upload_time'],
            datetime.datetime(year=2014, month=9, day=29, hour=23, minute=34, second=21)
        )

        updates = updatable.get_package_update_list('package2', '1.2.0')
        self.assertEqual(len(updates['minor_updates']), 1)
        self.assertEqual(
            updates['minor_updates'][0]['upload_time'],
            datetime.datetime(year=2015, month=9, day=29, hour=23, minute=34, second=21)
        )

        updates = updatable.get_package_update_list('package2', '1.3.0')
        self.assertEqual(len(updates['minor_updates']), 0)

    def test_patch_update_count(self):
        """
        Test update count for a package that has only patch releases
        """
        updates = updatable.get_package_update_list('package1', '1.0.0')
        self.assertEqual(updates['newer_releases'], 2)
        self.assertEqual(len(updates['major_updates']), 0)
        self.assertEqual(len(updates['minor_updates']), 0)
        self.assertEqual(len(updates['patch_updates']), 2)

        updates = updatable.get_package_update_list('package1', '1.0.1')
        self.assertEqual(updates['newer_releases'], 1)
        self.assertEqual(len(updates['major_updates']), 0)
        self.assertEqual(len(updates['minor_updates']), 0)
        self.assertEqual(len(updates['patch_updates']), 1)

        updates = updatable.get_package_update_list('package1', '1.0.2')
        self.assertEqual(updates['newer_releases'], 0)
        self.assertEqual(len(updates['major_updates']), 0)
        self.assertEqual(len(updates['minor_updates']), 0)
        self.assertEqual(len(updates['patch_updates']), 0)

    def test_patch_update_version(self):
        """
        Test update versions for a package that has only patch releases.
        This also shows that releases are ordered descendant by release date.
        """
        updates = updatable.get_package_update_list('package1', '1.0.0')
        self.assertEqual(len(updates['patch_updates']), 2)
        self.assertEqual(updates['patch_updates'][0]['version'], '1.0.2')
        self.assertEqual(updates['patch_updates'][1]['version'], '1.0.1')

        updates = updatable.get_package_update_list('package1', '1.0.1')
        self.assertEqual(len(updates['patch_updates']), 1)
        self.assertEqual(updates['patch_updates'][0]['version'], '1.0.2')

        updates = updatable.get_package_update_list('package1', '1.0.2')
        self.assertEqual(len(updates['patch_updates']), 0)

    def test_patch_update_date(self):
        """
        Test update upload time for a package that has only patch releases.
        This also shows that releases are ordered descendant by release date.
        """
        updates = updatable.get_package_update_list('package1', '1.0.0')
        self.assertEqual(len(updates['patch_updates']), 2)
        self.assertEqual(
            updates['patch_updates'][0]['upload_time'],
            datetime.datetime(year=2013, month=10, day=22, hour=23, minute=34, second=21)
        )
        self.assertEqual(
            updates['patch_updates'][1]['upload_time'],
            datetime.datetime(year=2013, month=9, day=29, hour=23, minute=34, second=21)
        )

        updates = updatable.get_package_update_list('package1', '1.0.1')
        self.assertEqual(len(updates['patch_updates']), 1)
        self.assertEqual(
            updates['patch_updates'][0]['upload_time'],
            datetime.datetime(year=2013, month=10, day=22, hour=23, minute=34, second=21)
        )

        updates = updatable.get_package_update_list('package1', '1.0.2')
        self.assertEqual(len(updates['patch_updates']), 0)

    def test_unusual_semantic_count(self):
        """
        Test for packages for a package with unusual versions
        """
        updates = updatable.get_package_update_list('package5', '0.9999999')
        self.assertEqual(updates['newer_releases'], 2)
        self.assertEqual(len(updates['major_updates']), 0)
        self.assertEqual(len(updates['minor_updates']), 2)
        self.assertEqual(len(updates['patch_updates']), 0)

        updates = updatable.get_package_update_list('package5', '0.99999999')
        self.assertEqual(updates['newer_releases'], 1)
        self.assertEqual(len(updates['major_updates']), 0)
        self.assertEqual(len(updates['minor_updates']), 1)
        self.assertEqual(len(updates['patch_updates']), 0)

        updates = updatable.get_package_update_list('package5', '0.999999999')
        self.assertEqual(updates['newer_releases'], 0)
        self.assertEqual(len(updates['major_updates']), 0)
        self.assertEqual(len(updates['minor_updates']), 0)
        self.assertEqual(len(updates['patch_updates']), 0)

    def test_non_semantic_count(self):
        """
        Test for package with non semantic verions
        """
        updates = updatable.get_package_update_list('package6', '0.1')
        self.assertEqual(updates['newer_releases'], 0)
        self.assertEqual(len(updates['major_updates']), 0)
        self.assertEqual(len(updates['minor_updates']), 0)
        self.assertEqual(len(updates['patch_updates']), 0)
        self.assertEqual(len(updates['non_semantic_versions']), 3)


if __name__ == '__main__':
    unittest.main()
