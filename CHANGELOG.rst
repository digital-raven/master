===========
 Changelog
===========
All notable changes to this software will be documented in this file.

The format is based on `Keep a Changelog <https://keepachangelog.com/en/1.0.0/>`_,
and this project adheres to `Semantic Versioning <https://semver.org/spec/v2.0.0.html>`_.

0.2.0 - 2022-07-28
==================

Added
-----
- Add Time Support to Tasks. Added a few more special fields to Tasks when
  processing as ICS events; start_time, due_time, and end_time.
- Added "duration" field.
- Task IDs now force an underscore.
- Comments to default configuration in init.
- New "todo" subcommand. Will look for tasks that have recurrance rules or
  due_date of "today" and print them out. If no time was specified then the
  command will list them as to be performed sometime throughout the day, and
  tasks that have specific times will be sorted by time.
    
Changed
-------
- Init projects using relative path. This has several advantages; like being
  able to use the project's path directly when printing what the path of tasks
  should be.
- "list" subcommand will omit tasks with a "closed" stage by default.
- Makes the output of the list subcommand more visually pleasing.
- Renamed the Project.listTasks method to filteredTasks, which is now a
  recursive generator.

Fixed
-----
- Task date comparisons. Filters like "t.due_date == 'today'" should work now.
- Bug during editing. master edit will now save the edited changes to the
  correct place.

Removed 
--------
- Removing default.ini in favor of a docstring. This allows easy copying of
  useful comments to the editor.

0.1.0 - 2022-05-12
==================
Changed the app's name to master to reflect more how a person may use this
program to master their time as well as their projects.

This release marks when master is basically useful; as in it may be used
in a basic case to init a project, add tasks to it, list those tasks based on
pythonic filters, and edit them.

There are bugs and unfriendly error messages in this release, and anything
about master's user experience may change, but at this point master may be
used to track its own effort.

Added
-----
- The add, edit, init, and list subcommands.
- The init subcommand will initialize a project on disk and open the project's
  conf for editing. The add subcommand will add tasks to that project, list
  will print the names of tasks which match a filter, and the output of list
  may be used directly as the argument for edit to view or edit said task.
- Project and Task classes. Tasks are stored on disk as rst files.
- Tab-autocomplete for the entire program.
- Unittests for Project and Task classes.

Changed
-------
- Changed name of application to "master".

Fixed
-----
- Dependent version of parsedatetime to be < 3.0.0

0.0.0 - 2022-04-11
==================
This is the initial tag. All changes to the project will be measured against
this tag. The app's name is "Work", but that will probably change.

Added
-----
- README and .gitignore.
