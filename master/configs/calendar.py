calendar = """\
################################################################################
# This configuration is for schedule-oriented events. Use the event_begin and
# duration / event_end fields to indicate the start times and durations of
# events for ICS calendar event exporting.
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
# Calendar events have a event_begin, duration, reccuring, and event_end
# behavior (daily, weekly...). Any tasks (not just ones under a project created
# with this template) that have a "event_begin" or "due_date" may be exported
# as ICS events.
#
# event_begin and event_end may be provided as human-readable datetime strings
# like "next week", or "next thursday 4pm"
#
# duration may be provided as hours and minutes. eg. "4h 30m".
#
# The recurring field follows ICS calendar rrule convention. As a bit of
# convenience, you may use a human-readable datetime to signify the end of
# the recurrance in the recurring_stop field.
#
default_attributes:
  event_begin:
  event_end:
  duration:
  recurring:
  recurring_stop:

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
