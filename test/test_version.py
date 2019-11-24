#!/usr/bin/env python
import os
import unittest
import semantic_version


package_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))


class TestVersion(unittest.TestCase):

    def test_package_version(self):
        about = {}
        with open(os.path.join(package_path, 'updatable', '__version__.py')) as f:
            exec(f.read(), about)

        self.assertTrue('__version__' in about)
        self.assertIsNotNone(about['__version__'])

        # Raises a ValueError if the new version is not semantic
        semantic_version.Version(about['__version__'])
