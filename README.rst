Updatable
=========

.. image:: https://travis-ci.org/nezhar/updatable.svg?branch=master
    :target: https://travis-ci.org/nezhar/updatable
.. image:: https://codecov.io/gh/nezhar/updatable/branch/master/graph/badge.svg
  :target: https://codecov.io/gh/nezhar/updatable

Updatable help you to find packages that require updates on a python environment.

Installation
~~~~~~~~~~~~

The latest release of updatable can be installed via PyPI:

::

    pip install -U updatable


It can be installed globally or in virtual environment, depending on where you plan to check the dependencies.
If you have a ``requirements.txt`` with pinned dependencies you can pass it as an argument to check against it.

The project supports Python ``2.7``, ``3.4``, ``3.5``, ``3.6``, ``3.7``, ``3.8`` as well as ``pypy`` and ``pypy3``.


Usage
~~~~~

The package can be used as a command line tool, so you can get a list of all
packages that require updates from your current environment. You may also use
the package inside of your python application, to list the packages over a REST
endpoint (see a `sample implementation here`__), forward them by mail or other purpose.

.. _Implementation: https://github.com/anexia-it/anexia-monitoring-django
__ Implementation_

Example
-------
::

    $> updatable

Prints:
::

    Django (2.1.13)
      Minor releases:
      -- 2.2.7 on 2019-11-04 08:33:19
      -- 2.2.6 on 2019-10-01 08:36:44
      -- 2.2.5 on 2019-09-02 07:18:39
      -- 2.2.4 on 2019-08-01 09:04:37
      -- 2.2.3 on 2019-07-01 07:19:23
      -- 2.2.2 on 2019-06-03 10:11:10
      -- 2.2.1 on 2019-05-01 06:57:39
      -- 2.2 on 2019-04-01 12:47:35
      Patch releases:
      -- 2.1.14 on 2019-11-04 08:33:13
    ___
    django-cors-headers (2.4.1)
      Major releases:
      -- 3.2.0 on 2019-11-15 10:28:47
      -- 3.1.1 on 2019-09-30 20:51:53
      -- 3.1.0 on 2019-08-13 08:12:02
      -- 3.0.2 on 2019-05-28 20:43:54
      -- 3.0.1 on 2019-05-13 13:00:40
      -- 3.0.0 on 2019-05-10 10:53:00
      Minor releases:
      -- 2.5.3 on 2019-04-28 19:03:35
      -- 2.5.2 on 2019-03-15 16:42:57
      -- 2.5.1 on 2019-03-13 13:03:04
      -- 2.5.0 on 2019-03-05 11:41:22
      Unknown releases:
      -- 0.01 on 2013-01-19 20:19:21
      -- 0.02 on 2013-01-19 22:19:24
      -- 0.03 on 2013-01-22 08:37:28
      -- 0.04 on 2013-01-25 05:35:38
      -- 0.05 on 2013-01-25 22:57:40
      -- 0.06 on 2013-02-21 18:39:33
    ___
    Jinja2 (2.10.1)
      Patch releases:
      -- 2.10.3 on 2019-10-04 18:52:37
      -- 2.10.2 on 2019-10-04 18:19:47
    ___
    Markdown (3.0.1)
      Minor releases:
      -- 3.1.1 on 2019-05-21 01:10:24
      -- 3.1 on 2019-03-26 00:20:04
    ___
    pytz (2019.2)
      Minor releases:
      -- 2019.3 on 2019-10-07 03:18:16
    ___
    urllib3 (1.25.6)
      Patch releases:
      -- 1.25.7 on 2019-11-11 15:10:09


Console Parameters
------------------
The console program offers the following parameters:

::

    -f <filename>
    --file <filename>

Optionally defines a requirements file to use.

If the parameter is not defined, the packages of the current Python environment will be used.

::

    -pre <boolean>
    --pre-releases <boolean>

Includes pre-releases in the output, as separate category.

Default: false

Acceptable boolean values:
::

    Positive: yes, true, t, y, 1
    Negative: no, false, f, n, 0

Example using both parameters
-----------------------------
::

    $> updatable -f requirements.txt --pre-releases yes

Development
~~~~~~~~~~~

Add pre-commit package:
::

    pip install pre-commit

Install pre-commit hook:
::

    pre-commit install
