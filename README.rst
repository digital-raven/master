========
 master
========

Welcome to master, a program for for mastering projects and time management.

Usage
=====
Usage is detailed in the man pages under ``./doc/man``.

Maintenance
===========
Update the CHANGELOG and version in setup.py when cutting a new release,
then create and push a git tag named after the new version.

Building and installation
=========================
Run ``make`` to build the package.

Testing and developer usage
===========================
Run these commands to install master to a virtual environment.

::

    python3 -m venv ./venv
    . ./venv/bin/activate
    python3 ./setup.py
    pip3 install -e .
    master

Use the following command to run unit tests.

::

    python3 -m unittest
