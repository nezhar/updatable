#!/usr/bin/env python
import asyncio
import sys
import unittest
from argparse import ArgumentTypeError
from io import StringIO
from test.utils import TEST_REQUIREMENTS_PATH, get_environment_requirements_list_monkey
from unittest.mock import patch

from updatable.console import _argument_parser, _list_package_updates, _list_updates, _str_to_bool, _updatable


class Capture(list):
    def __enter__(self):
        self._stdout = sys.stdout
        sys.stdout = self._stringio = StringIO()
        return self

    def __exit__(self, *args):
        self.extend(self._stringio.getvalue().splitlines())
        del self._stringio  # free up memory
        sys.stdout = self._stdout


class TestStrToBool(unittest.TestCase):
    def test_str_to_bool_true(self):
        self.assertTrue(_str_to_bool(True))
        self.assertTrue(_str_to_bool("t"))
        self.assertTrue(_str_to_bool("y"))
        self.assertTrue(_str_to_bool("True"))
        self.assertTrue(_str_to_bool("YES"))
        self.assertTrue(_str_to_bool("1"))

    def test_str_to_bool_false(self):
        self.assertFalse(_str_to_bool(False))
        self.assertFalse(_str_to_bool("f"))
        self.assertFalse(_str_to_bool("n"))
        self.assertFalse(_str_to_bool("False"))
        self.assertFalse(_str_to_bool("NO"))
        self.assertFalse(_str_to_bool("0"))

    def test_str_to_bool_exception(self):
        with self.assertRaises(ArgumentTypeError):
            _str_to_bool("")

        with self.assertRaises(ArgumentTypeError):
            _str_to_bool("falsy")

        with self.assertRaises(ArgumentTypeError):
            _str_to_bool("eye")


class TestListUpdates(unittest.TestCase):
    def test_with_empty_list(self):
        with Capture() as output:
            _list_updates("Test", [], "MIT")

        self.assertListEqual(output, [])

    def test_with_updates_in_list(self):
        with Capture() as output:
            _list_updates(
                "Test",
                [
                    {"version": "1.0.0", "upload_time": "date 1"},
                    {"version": "2.0.0", "upload_time": "date 2"},
                ],
                "MIT",
            )

        self.assertListEqual(
            output,
            [
                "  Test:",
                "  -- 1.0.0 on date 1 - License: MIT",
                "  -- 2.0.0 on date 2 - License: MIT",
            ],
        )


class TestListPackageUpdates(unittest.TestCase):
    async def _mock_get_package_update_list(*args, **kwargs):

        # No updates, no prereeases, no non semantic version
        if args[1] == "package1":
            return {
                "newer_releases": 0,
                "pre_releases": 0,
                "major_updates": [],
                "minor_updates": [],
                "patch_updates": [],
                "pre_release_updates": [],
                "non_semantic_versions": [],
                "current_release_license": "MIT",
            }

        # Updates, no prereeases, no non semantic version
        if args[1] == "package2":
            return {
                "newer_releases": 5,
                "pre_releases": 0,
                "major_updates": [
                    {"version": "2.0.0", "upload_time": "date 3"},
                    {"version": "3.0.0", "upload_time": "date 5"},
                ],
                "minor_updates": [
                    {"version": "1.5.0", "upload_time": "date 2"},
                    {"version": "2.5.0", "upload_time": "date 4"},
                ],
                "patch_updates": [
                    {"version": "1.5.5", "upload_time": "date 5"},
                ],
                "pre_release_updates": [],
                "non_semantic_versions": [],
                "current_release_license": "MIT",
            }

        # Updates, no prereeases, non semantic version
        if args[1] == "package3":
            return {
                "newer_releases": 1,
                "pre_releases": 0,
                "major_updates": [],
                "minor_updates": [],
                "patch_updates": [
                    {"version": "1.5.5", "upload_time": "date 5"},
                ],
                "pre_release_updates": [],
                "non_semantic_versions": [
                    {"version": "test1.5.5.3.2.3.23", "upload_time": "date 6"},
                ],
                "current_release_license": "MIT",
            }

        # Updates, prereeases, non semantic version
        if args[1] == "package4":
            return {
                "newer_releases": 1,
                "pre_releases": 1,
                "major_updates": [],
                "minor_updates": [],
                "patch_updates": [
                    {"version": "1.5.5", "upload_time": "date 5"},
                ],
                "pre_release_updates": [
                    {"version": "alfa-1.5.5", "upload_time": "date 7"},
                ],
                "non_semantic_versions": [
                    {"version": "test1.5.5.3.2.3.23", "upload_time": "date 6"},
                ],
                "current_release_license": "MIT",
            }

        # No updates, prereeases, non semantic version
        if args[1] == "package5":
            return {
                "newer_releases": 0,
                "pre_releases": 1,
                "major_updates": [],
                "minor_updates": [],
                "patch_updates": [],
                "pre_release_updates": [
                    {"version": "alfa-1.5.5", "upload_time": "date 7"},
                ],
                "non_semantic_versions": [
                    {"version": "test1.5.5.3.2.3.23", "upload_time": "date 6"},
                ],
                "current_release_license": "MIT",
            }

        # Pre releases only
        if args[1] == "package6":
            return {
                "newer_releases": 0,
                "pre_releases": 1,
                "major_updates": [],
                "minor_updates": [],
                "patch_updates": [],
                "pre_release_updates": [
                    {"version": "alfa-1.5.5", "upload_time": "date 7"},
                ],
                "non_semantic_versions": [],
                "current_release_license": "MIT",
            }

        # Non semantic version only
        if args[1] == "package7":
            return {
                "newer_releases": 0,
                "pre_releases": 0,
                "major_updates": [],
                "minor_updates": [],
                "patch_updates": [],
                "pre_release_updates": [],
                "non_semantic_versions": [
                    {"version": "test1.5.5.3.2.3.23", "upload_time": "date 6"},
                ],
                "current_release_license": "MIT",
            }

    def _mock_argument_parser(*args, **kwargs):
        class MockResult:
            file = get_environment_requirements_list_monkey()
            pre_releases = False

        class ArgumentParserMock:
            def parse_args(*args, **kwargs):
                return MockResult()

        return ArgumentParserMock()

    def test_with_no_available_updates(self):
        with patch(
            "updatable.utils.get_package_update_list",
            side_effect=self._mock_get_package_update_list,
        ):
            with Capture() as output:
                asyncio.run(_list_package_updates("package1", "1.0.0", False))
            self.assertListEqual(output, [])

            with Capture() as output:
                asyncio.run(_list_package_updates("package1", "1.0.0", True))
            self.assertListEqual(output, [])

    def test_with_updates_and_no_prereleases(self):
        with patch(
            "updatable.utils.get_package_update_list",
            side_effect=self._mock_get_package_update_list,
        ):
            with Capture() as output:
                asyncio.run(_list_package_updates("package2", "1.0.0", False))
            self.assertListEqual(
                output,
                [
                    "package2 (1.0.0) - License: MIT",
                    "  Major releases:",
                    "  -- 2.0.0 on date 3 - License: MIT",
                    "  -- 3.0.0 on date 5 - License: MIT",
                    "  Minor releases:",
                    "  -- 1.5.0 on date 2 - License: MIT",
                    "  -- 2.5.0 on date 4 - License: MIT",
                    "  Patch releases:",
                    "  -- 1.5.5 on date 5 - License: MIT",
                    "___",
                ],
            )

            with Capture() as output:
                asyncio.run(_list_package_updates("package2", "1.0.0", True))
            self.assertListEqual(
                output,
                [
                    "package2 (1.0.0) - License: MIT",
                    "  Major releases:",
                    "  -- 2.0.0 on date 3 - License: MIT",
                    "  -- 3.0.0 on date 5 - License: MIT",
                    "  Minor releases:",
                    "  -- 1.5.0 on date 2 - License: MIT",
                    "  -- 2.5.0 on date 4 - License: MIT",
                    "  Patch releases:",
                    "  -- 1.5.5 on date 5 - License: MIT",
                    "___",
                ],
            )

    def test_with_updates_and_no_prereleases_and_non_semantic_versions(self):
        with patch(
            "updatable.utils.get_package_update_list",
            side_effect=self._mock_get_package_update_list,
        ):
            with Capture() as output:
                asyncio.run(_list_package_updates("package3", "1.0.0", False))
            self.assertListEqual(
                output,
                [
                    "package3 (1.0.0) - License: MIT",
                    "  Patch releases:",
                    "  -- 1.5.5 on date 5 - License: MIT",
                    "  Unknown releases:",
                    "  -- test1.5.5.3.2.3.23 on date 6 - License: MIT",
                    "___",
                ],
            )

            with Capture() as output:
                asyncio.run(_list_package_updates("package3", "1.0.0", True))
            self.assertListEqual(
                output,
                [
                    "package3 (1.0.0) - License: MIT",
                    "  Patch releases:",
                    "  -- 1.5.5 on date 5 - License: MIT",
                    "  Unknown releases:",
                    "  -- test1.5.5.3.2.3.23 on date 6 - License: MIT",
                    "___",
                ],
            )

    def test_with_updates_and_prereleases_and_non_semantic_versions(self):
        with patch(
            "updatable.utils.get_package_update_list",
            side_effect=self._mock_get_package_update_list,
        ):
            with Capture() as output:
                asyncio.run(_list_package_updates("package4", "1.0.0", False))
            self.assertListEqual(
                output,
                [
                    "package4 (1.0.0) - License: MIT",
                    "  Patch releases:",
                    "  -- 1.5.5 on date 5 - License: MIT",
                    "  Unknown releases:",
                    "  -- test1.5.5.3.2.3.23 on date 6 - License: MIT",
                    "___",
                ],
            )

            with Capture() as output:
                asyncio.run(_list_package_updates("package4", "1.0.0", True))
            self.assertListEqual(
                output,
                [
                    "package4 (1.0.0) - License: MIT",
                    "  Patch releases:",
                    "  -- 1.5.5 on date 5 - License: MIT",
                    "  Unknown releases:",
                    "  -- test1.5.5.3.2.3.23 on date 6 - License: MIT",
                    "  Pre releases:",
                    "  -- alfa-1.5.5 on date 7 - License: MIT",
                    "___",
                ],
            )

    def test_with_prereleases_and_non_semantic_versions(self):
        with patch(
            "updatable.utils.get_package_update_list",
            side_effect=self._mock_get_package_update_list,
        ):
            with Capture() as output:
                asyncio.run(_list_package_updates("package5", "1.0.0", False))
            self.assertListEqual(output, [])

            with Capture() as output:
                asyncio.run(_list_package_updates("package5", "1.0.0", True))
            self.assertListEqual(
                output,
                [
                    "package5 (1.0.0) - License: MIT",
                    "  Pre releases:",
                    "  -- alfa-1.5.5 on date 7 - License: MIT",
                    "___",
                ],
            )

    def test_with_prereleases(self):
        with patch(
            "updatable.utils.get_package_update_list",
            side_effect=self._mock_get_package_update_list,
        ):
            with Capture() as output:
                asyncio.run(_list_package_updates("package6", "1.0.0", False))
            self.assertListEqual(output, [])

            with Capture() as output:
                asyncio.run(_list_package_updates("package6", "1.0.0", True))
            self.assertListEqual(
                output,
                [
                    "package6 (1.0.0) - License: MIT",
                    "  Pre releases:",
                    "  -- alfa-1.5.5 on date 7 - License: MIT",
                    "___",
                ],
            )

    def test_with_non_semantic_versions(self):
        with patch(
            "updatable.utils.get_package_update_list",
            side_effect=self._mock_get_package_update_list,
        ):
            with Capture() as output:
                asyncio.run(_list_package_updates("package7", "1.0.0", False))
            self.assertListEqual(output, [])

            with Capture() as output:
                asyncio.run(_list_package_updates("package7", "1.0.0", True))
            self.assertListEqual(output, [])

    def test_updatable_call(self):
        with patch("updatable.console._argument_parser", side_effect=self._mock_argument_parser):
            with patch(
                "updatable.utils.get_package_update_list",
                side_effect=self._mock_get_package_update_list,
            ):
                with Capture() as output:
                    asyncio.run(_updatable())

                self.assertListEqual(
                    output,
                    [
                        "package2 (1.0) - License: MIT",
                        "  Major releases:",
                        "  -- 2.0.0 on date 3 - License: MIT",
                        "  -- 3.0.0 on date 5 - License: MIT",
                        "  Minor releases:",
                        "  -- 1.5.0 on date 2 - License: MIT",
                        "  -- 2.5.0 on date 4 - License: MIT",
                        "  Patch releases:",
                        "  -- 1.5.5 on date 5 - License: MIT",
                        "___",
                        "package3 (2) - License: MIT",
                        "  Patch releases:",
                        "  -- 1.5.5 on date 5 - License: MIT",
                        "  Unknown releases:",
                        "  -- test1.5.5.3.2.3.23 on date 6 - License: MIT",
                        "___",
                        "package4 (2.4) - License: MIT",
                        "  Patch releases:",
                        "  -- 1.5.5 on date 5 - License: MIT",
                        "  Unknown releases:",
                        "  -- test1.5.5.3.2.3.23 on date 6 - License: MIT",
                        "___",
                    ],
                )


class TestArgumentParser(unittest.TestCase):
    def setUp(self):
        self.parser = _argument_parser()

    def test_argument_parser_pre_release(self):
        # Long param
        parsed = self.parser.parse_args(["--pre-release", "True"])
        self.assertEqual(parsed.pre_releases, True)

        parsed = self.parser.parse_args(["--pre-release", "Yes"])
        self.assertEqual(parsed.pre_releases, True)

        parsed = self.parser.parse_args(["--pre-release", "T"])
        self.assertEqual(parsed.pre_releases, True)

        parsed = self.parser.parse_args(["--pre-release", "t"])
        self.assertEqual(parsed.pre_releases, True)

        parsed = self.parser.parse_args(["--pre-release", "1"])
        self.assertEqual(parsed.pre_releases, True)

        parsed = self.parser.parse_args(["--pre-release", "TrUe"])
        self.assertEqual(parsed.pre_releases, True)

        parsed = self.parser.parse_args(["--pre-release", "f"])
        self.assertEqual(parsed.pre_releases, False)

        parsed = self.parser.parse_args(["--pre-release", "n"])
        self.assertEqual(parsed.pre_releases, False)

        parsed = self.parser.parse_args(["--pre-release", "0"])
        self.assertEqual(parsed.pre_releases, False)

        parsed = self.parser.parse_args(["--pre-release", "FaLse"])
        self.assertEqual(parsed.pre_releases, False)

        with self.assertRaises(SystemExit):
            self.parser.parse_args(["--pre-release", "Invalid"])

        # Short param
        parsed = self.parser.parse_args(["-pr", "True"])
        self.assertEqual(parsed.pre_releases, True)

        parsed = self.parser.parse_args(["-pr", "Yes"])
        self.assertEqual(parsed.pre_releases, True)

        parsed = self.parser.parse_args(["-pr", "T"])
        self.assertEqual(parsed.pre_releases, True)

        parsed = self.parser.parse_args(["-pr", "t"])
        self.assertEqual(parsed.pre_releases, True)

        parsed = self.parser.parse_args(["-pr", "1"])
        self.assertEqual(parsed.pre_releases, True)

        parsed = self.parser.parse_args(["-pr", "TrUe"])
        self.assertEqual(parsed.pre_releases, True)

        parsed = self.parser.parse_args(["-pr", "f"])
        self.assertEqual(parsed.pre_releases, False)

        parsed = self.parser.parse_args(["-pr", "n"])
        self.assertEqual(parsed.pre_releases, False)

        parsed = self.parser.parse_args(["-pr", "0"])
        self.assertEqual(parsed.pre_releases, False)

        parsed = self.parser.parse_args(["-pr", "FaLse"])
        self.assertEqual(parsed.pre_releases, False)

        with self.assertRaises(SystemExit):
            self.parser.parse_args(["-pr", "Invalid"])

    def test_invalid_argument(self):
        with self.assertRaises(SystemExit):
            self.parser.parse_args(["--invalid", "Value"])

    def test_argument_parser_pre_file(self):
        # Long param
        parsed = self.parser.parse_args(["--file", TEST_REQUIREMENTS_PATH])

        self.assertEqual(
            list(parsed.file),
            [
                "package1==0.1\n",
                "package2==1.0\n",
                "package3==2\n",
                "package4==2.4\n",
                "package5==3.0.0\n",
            ],
        )

        with self.assertRaises(SystemExit):
            self.parser.parse_args(["--file", "Invalid"])

        # Short param
        parsed = self.parser.parse_args(["-f", TEST_REQUIREMENTS_PATH])

        self.assertEqual(
            list(parsed.file),
            [
                "package1==0.1\n",
                "package2==1.0\n",
                "package3==2\n",
                "package4==2.4\n",
                "package5==3.0.0\n",
            ],
        )

        with self.assertRaises(SystemExit):
            self.parser.parse_args(["-f", "Invalid"])


if __name__ == "__main__":
    unittest.main()
