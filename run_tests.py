import unittest
import doctest


def test_suite():
    suite = unittest.TestLoader().discover("test")
    suite.addTest(doctest.DocFileSuite("README.rst"))
    return suite


if __name__ == "__main__":
    unittest.TextTestRunner(verbosity=2).run(test_suite())
