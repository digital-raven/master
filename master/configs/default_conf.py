default_conf = """\
################################################################################
# This is the default configuration for new projects. The settings
# in this file will be copied to new projects as .master.project
#

################################################################################
# List of users who have ultimate access to this project and every
# project below this level.
#
owners = __DEFAULT_OWNER

################################################################################
# Name of the project. Will be named after the basename of the
# containing folder by default, but may be changed later.
#
project_name = __DEFAULT_PROJECT_NAME

################################################################################
# Attributes that each new task under this project will have by default. Place
# each attribute on its own line.
#
# Each task will always have a creation_date, creator, id, project, stage,
# and tags regardless of the defaults listed here.
#
default_attributes =
    creation_date
    creator
    id
    project
    stage
    tags

################################################################################
# Default attribute values for new tasks. Each default should be on its
# own line. Multiline values are not supported. eg...
#
#   default_attribute_values =
#       stage: todo
#       due_date: next wednesday
#
# This setting cannot override the creation_date, creator, id, or project
# attributes, as those are generated automatically for each task.
#
default_attribute_values =
    stage: todo

################################################################################
# Used to prefix the IDs of tasks created within the project.
#
# This will default to the first few characters (4 or fewer) of the project's
# name, but may be changed later.
#
task_prefix = __DEFAULT_PREFIX
"""