Description
===========

Framework for testing ebuilds.

Using Docker to provide consistent sandboxed environments, etest runs ebuilds
through several tests (implicitly and explicitly defined).  Every ebuild gets
two containers created to install a testing and non-testing version (FEATURES
with and without test) as well as any other commands specified for that ebuild
with the particular USE flags.

Installation
============

This package is stored in PyPI and can be installed the standard way::

    pip install etest

The latest release available is:

.. image:: https://badge.fury.io/py/etest.png
    :target: http://badge.fury.io/py/etest

Using etest
===========

Usage of this package is outlined in the documentation::

    etest --help

Developing etest
================

If you would prefer to clone this package directly from git or assist with 
development, the URL is https://github.com/alunduil/etest.

etest is tested continuously by Travis-CI and running the tests is quite 
simple::

    flake8
    nosetests

The current status of the build is:

.. image:: https://secure.travis-ci.org/alunduil/etest.png?branch=master
   :target: http://travis-ci.org/alunduil/etest

Authors
=======

* Alex Brandt <alunduil@gentoo.org>

Known Issues
============

Known issues can be found in the github issue list at
https://github.com/alunduil/crumbs/etest.

Troubleshooting
===============

If you need to troubleshoot an issue or submit information in a bug report, we
recommend obtaining the following pieces of information:

* output with very verbose output turned on
* any relevant stack traces
