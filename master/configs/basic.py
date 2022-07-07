basic = """\
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
# Attributes that each new task under this project will have by default.
#
# Each task will always have a creation_date, creator, id, project,
# and tags regardless of the defaults listed here.
#
default_attributes:
  creation_date:
  creator:
  id:
  project:
  stage: todo
  tags:

################################################################################
# Used to prefix the IDs of tasks created within the project.
#
# This will default to the first few characters (4 or fewer) of the project's
# name, but may be changed later.
#
# If task_prefix is '__date' then new tasks will have their prefixs (and thus
# their filenames and IDs) be interpreted as a date or datetime.
#
task_prefix: __DEFAULT_PREFIX
"""
