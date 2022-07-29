note = """\
################################################################################
# This is a configuration for projects with basic tasks. The settings
# in this file will be copied to new projects as project.yaml
#
# Settings in this string that begin with a double underscore are automatically
# replaced when the real project configuration is created.
#

################################################################################
# List of users who have ultimate access to this project and every
# project below this level.
#
owners:
  - __DEFAULT_OWNER

################################################################################
# Name of the project. Will be named after the basename of the
# containing folder by default.
#
project_name: __DEFAULT_PROJECT_NAME

################################################################################
# Attributes that each new task under this project will have by default. Each
# task will always have a creation_date, creator, id, project, and tags
# regardless of the defaults listed here.
#
# A basic task only adds on a due_date and stage. The only stage value reserved
# by master is "closed". "closed" tasks are omitted from master filters by
# default. Feel free to use any other values for your own task progressions.
#
default_attributes:

################################################################################
# Used to prefix the IDs of tasks created within the project.
#
# This will default to the first few characters of the project's name.
#
# If task_prefix is '__date' then new tasks will have their prefixs (and thus
# their filenames and IDs) be interpreted as a date or datetime.
#
task_prefix: __DEFAULT_PREFIX
"""
