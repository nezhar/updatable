import os
import io

from setuptools import find_packages, setup

# Package meta-data.
NAME = 'updatable'
DESCRIPTION = 'Finds packages that require updates on a python environment.'
URL = 'https://github.com/nezhar/updatable'
EMAIL = 'hn@nezhar.com'
AUTHOR = 'Harald Nezbeda'

# What packages are required for this module to be executed?
REQUIRED = [
    'requests',
    'semantic_version',
    'pyopenssl',
    'packaging',
]

# Setup configuration
current_path = os.path.abspath(os.path.dirname(__file__))

# Import the README and use it as the long-description.
# Note: this will only work if 'README.rst' is present in your MANIFEST.in file!
with io.open(os.path.join(current_path, 'README.rst'), encoding='utf-8') as f:
    long_description = '\n' + f.read()

setup(
    name=NAME,
    version=os.getenv('PACKAGE_VERSION', '0.0.0').replace('refs/tags/', ''),
    description=DESCRIPTION,
    long_description=long_description,
    author=AUTHOR,
    author_email=EMAIL,
    url=URL,
    packages=find_packages(exclude=('test',)),
    entry_points={
        'console_scripts': [
            'updatable = updatable.console:_updatable',
        ]
    },
    install_requires=REQUIRED,
    include_package_data=True,
    license='MIT',
    classifiers=[
        # Trove classifiers
        # Full list: https://pypi.python.org/pypi?%3Aaction=list_classifiers
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Natural Language :: English',
        'Topic :: Utilities',
    ],
)
