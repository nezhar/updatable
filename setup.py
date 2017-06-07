import os

from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='updatable',
    version='0.1.4',
    packages=find_packages(),
    include_package_data=True,
    license='MIT License',
    description='Finds packages that require updates on a python environment.',
    long_description=README,
    url='http://nezhar.com/',
    author='Harald Nezbeda',
    author_email='hn@nezhar.com',
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Natural Language :: English',
        'Topic :: Utilities',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
    ],
    install_requires=[
        'requests',
        'semantic_version',
        'pyopenssl',
    ],
    entry_points={
        'console_scripts': [
            'updatable = updatable:__updatable',
        ]
    },
)
