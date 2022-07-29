calendar = """\
################################################################################
# This configuration is for schedule-oriented events. Use the start_date and
# duration fields to indicate the start times and durations of events for
# ICS calendar event exporting, and end_date to pair with recurring if a
# recurring event should stop on a given date.
#

################################################################################
# List of users who have ultimate access to this project and every
# project below this level.
#
owners:
  - __DEFAULT_OWNER

################################################################################
# This project be named after the basename of the containing folder by default.
#
project_name: __DEFAULT_PROJECT_NAME

################################################################################
# Attributes that each new task under this project will have by default. Each
# task will always have a creation_date, creator, id, project, and tags
# regardless of the defaults listed here.
#
# Calendar events have a start_date, duration, reccuring, and end_date
# behavior (daily, weekly...). Any tasks (not just ones under a project created
# with this template) that have a "start_date" or "due_date" may be exported
# as ICS events.
#
# start_date and end_date may be provided as human-readable datetime strings
# like "next week", or "next thursday 4pm"
#
# duration may be provided as hours and minutes. eg. "4h 30m".
#
# The recurring field needs to follow the ICS recurrance rules.
#
default_attributes:
  end_date: 
  duration:
  recurring:
  start_date:

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
