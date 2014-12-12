Description
===========

Framework for testing ebuilds.

Using Docker to provide consistent sandboxed environments, etest runs ebuilds
through several tests (implicitly and explicitly defined).  Every ebuild gets
many containers created to run every testing scenario in isolation.  Testing
scenarios are created from combinations of USE flags, features (test or no
test), as well as custom commands provided in the hints files.

Installation
============

This package is available in my overlay, alunduil, and can be installed on
Gentoo quite easily::

    layman -a alunduil
    emerge app-portage/etest

This package is also stored in PyPI and can be installed the standard way::

    pip install etest

The latest release available is:

.. image:: https://badge.fury.io/py/etest.png
    :target: http://badge.fury.io/py/etest


 ``etest`` does require a running docker daemon but does not explicitly list it
 as a requirement.

Using etest
===========

.. note::
    etest requires a running docker daemon (either local or remote).  If using
    a remote docker instance you must set the DOCKER_HOST environment variable
    with the hostname (just like fig).

To get started simply run ``etest`` in a directory that contains ebuilds in a
valid overlay.

Alternatively, while still in a valid overlay directory or subdirectory, a list
of ebuilds can be passed to ``etest`` to run tests only against those ebuilds::

    # Run all etest tests for all ebuild versions.
    cd /var/lib/layman/alunduil
    etest app-portage/etest

    # Run all etest tests for the specified ebuild.
    cd app-portage/etest
    etest etest-9999.ebuild

More advanced usage of this package is outlined in the built-in help::

    etest --help

Developing etest
================

If you would prefer to clone this package directly from git or assist with 
development, the URL is https://github.com/alunduil/etest.

etest is tested continuously by Travis-CI and running the tests is quite 
simple::

    flake8
    nosetests test_etest/test_unit

System tests can be run as well but require a working docker daemon as well as
approximately two and half hours::

    nosetests test_etest/test_system

The current status of the build is:

.. image:: https://secure.travis-ci.org/alunduil/etest.png?branch=master
   :target: http://travis-ci.org/alunduil/etest

Authors
=======

* Alex Brandt <alunduil@gentoo.org>

Known Issues
============

Known issues can be found in the github issue list at
https://github.com/alunduil/etest/issues.

Troubleshooting
===============

If you need to troubleshoot an issue or submit information in a bug report, we
recommend obtaining the following pieces of information:

* output with verbose output turned on
* any relevant stack traces
