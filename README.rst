========
 master
========

Welcome to master, a program for for mastering projects and time management.

Usage
=====
Usage is detailed in the man pages under ``./doc/man``.

Description
===========
I have a personal interest in managing my notes as files on my system in
a simple markdown format. Master is the program I wrote as a tool to help
make this effort more convenient.

For now its operations are basic in creating and editing these files, but
there is a structure for todos, templates so new entries may have default
attributes, and the ability to create new notes as tickets with unique
identifiers in the title.

Future development
------------------
This is a personal project that I use for myself. I plan on adding link
suggestion and the ability for notes to automatically update their links
when their location on the file system changes.

But for now the interface of the zettels is stable. They use the libzet
format, and I will not be changing their format.

Maintenance
===========
Update the CHANGELOG and version in setup.py when cutting a new release,
then create and push a git tag named after the new version.

Building and installation
=========================
Run ``make`` to build the package.

Testing and developer usage
===========================
Use the following command to run unit tests.

::

    python3 -m unittest
