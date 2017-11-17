Updatable
=========

.. image:: https://travis-ci.org/nezhar/updatable.svg?branch=master
    :target: https://travis-ci.org/nezhar/updatable

Finds packages that require updates on a python environment

Installation
~~~~~~~~~~~~

The latest release of updatable can be installed via PyPI:

::

    pip install -U updatable


Usage
~~~~~

The package can be used as a command line tool, so you can get a list of all
packages that require updates from your current environment. You may also use
the package inside of your python application, to list the packages over a REST
endpoint, forward them by mail or other purpose.

Example:
::

    $> updatable

Prints:


::


    Babel (2.4.0)
      Minor releases:
      -- 2.5.1 on 2017-09-14 10:11:05
      -- 2.5.0 on 2017-08-18 09:06:43
    ___
    CairoSVG (2.1.1)
      Pre releases:
      -- 2.0.0rc6 on 2016-08-27 13:33:39
      -- 2.0.0rc5 on 2016-08-05 15:23:18
      -- 2.0.0rc4 on 2016-07-16 17:02:21
      -- 2.0.0rc3 on 2016-07-16 16:48:34
      -- 2.0.0rc2 on 2016-06-14 16:08:00
      -- 2.0.0rc1 on 2016-04-30 10:11:02
    ___
    certifi (2017.7.27.1)
      Minor releases:
      -- 2017.11.5 on 2017-11-05 13:22:40
      Unknown releases:
      -- 14.05.14 on 2014-05-18 22:55:55
      -- 2015.04.28 on 2015-04-28 17:40:47
    ___
    cryptography (2.1.1)
      Patch releases:
      -- 2.1.3 on 2017-11-02 19:03:54
      -- 2.1.2 on 2017-10-24 15:50:02
    ___
    Django (1.11.6)
      Patch releases:
      -- 1.11.7 on 2017-11-02 01:26:27
      Pre releases:
      -- 2.0b1 on 2017-10-17 02:00:54
      -- 2.0a1 on 2017-09-22 18:09:22
      -- 1.11rc1 on 2017-03-21 22:55:53
      -- 1.11b1 on 2017-02-20 23:21:50
      -- 1.11a1 on 2017-01-18 01:01:35
      -- 1.10rc1 on 2016-07-18 18:04:51
      -- 1.10b1 on 2016-06-22 01:15:05
      -- 1.10a1 on 2016-05-20 12:16:44
      -- 1.9rc2 on 2015-11-24 17:35:35
      -- 1.9rc1 on 2015-11-16 21:10:10
      -- 1.9b1 on 2015-10-20 01:17:13
      -- 1.9a1 on 2015-09-24 00:20:01
      -- 1.8c1 on 2015-03-18 23:39:34
      -- 1.8b2 on 2015-03-09 15:55:16
      -- 1.8b1 on 2015-02-25 13:42:42
      -- 1.8a1 on 2015-01-16 22:25:13
    ___
    django-auth-ldap (1.2.16)
      Pre releases:
      -- 1.3.0b3 on 2017-10-15 20:37:57
      -- 1.3.0b2 on 2017-09-26 18:05:41
      -- 1.3.0b1 on 2017-09-11 18:18:07
      -- 1.2.14b1 on 2017-07-21 16:48:55
    ___
    django-ckeditor (5.2.2)
      Minor releases:
      -- 5.3.1 on 2017-10-25 07:55:10
      -- 5.3.0 on 2017-06-30 16:48:13
    ___
    django-debug-toolbar (1.8)
      Minor releases:
      -- 1.9 on 2017-11-13 19:42:06
    ___
    django-filter (1.1.0)
      Pre releases:
      -- 2.0.0.dev1 on 2017-10-24 10:09:20
      -- 0.6a1 on 2013-03-12 18:46:48
    ___
    django-redis-cache (1.7.1)
      Pre releases:
      -- 1.0.0a on 2015-06-24 05:54:48
    ___
    djangorestframework (3.7.1)
      Patch releases:
      -- 3.7.3 on 2017-11-06 15:35:29
      -- 3.7.2 on 2017-11-06 11:06:34


