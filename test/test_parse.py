#!/usr/bin/env python
import unittest
import os

from updatable import utils as updatable_utils


PATH = os.path.dirname(os.path.realpath(__file__))


def get_environment_requirements_list_monkey(*args, **kwargs):
    with open(os.path.join(PATH, 'fixtures/requirements-initial.txt')) as f:
        content = f.readlines()

    return content


class TestParse(unittest.TestCase):

    def setUp(self):
        self.get_environment_requirements_list_orig = updatable_utils.get_environment_requirements_list
        updatable_utils.get_environment_requirements_list = get_environment_requirements_list_monkey

    def tearDown(self):
        updatable_utils.get_environment_requirements_list = self.get_environment_requirements_list_orig

    def assert_package_list(self, packages):
        """
        Test if the requirements are parsed correctly

        :param packages: dict
        """
        self.assertEqual(len(packages), 5)

        self.assertEqual(packages[0]['version'], '0.1')
        self.assertEqual(packages[1]['version'], '1.0')
        self.assertEqual(packages[2]['version'], '2')
        self.assertEqual(packages[3]['version'], '2.4')
        self.assertEqual(packages[4]['version'], '3.0.0')

        self.assertEqual(packages[0]['package'], 'package1')
        self.assertEqual(packages[1]['package'], 'package2')
        self.assertEqual(packages[2]['package'], 'package3')
        self.assertEqual(packages[3]['package'], 'package4')
        self.assertEqual(packages[4]['package'], 'package5')

    def test_get_parsed_environment_package_list(self):
        """
        Test parsing requirements from environment
        """
        packages = updatable_utils.get_parsed_environment_package_list()
        self.assert_package_list(packages)

    def test_parse_requirements_list(self):
        """
        Test parsing requirements list
        """
        requirements_list = ['package1==0.1', 'package2==1.0', 'package3==2', 'package4==2.4', 'package5==3.0.0', ]
        packages = updatable_utils.parse_requirements_list(requirements_list)
        self.assert_package_list(packages)


if __name__ == '__main__':
    unittest.main()
