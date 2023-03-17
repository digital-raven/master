calendar = """\
################################################################################
# This configuration is for schedule-oriented events. Tasks created here are
# designed to be exported as generic ICS events; usable with other calendars.
#

# Default zettel format: md or rst
zettel_format: md

# Default headings for new tasks
headings: []

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
attrs:
  event_begin:
  event_end:
  duration:
  project_name: __DEFAULT_PROJECT_NAME
  recurring:
  recurring_stop:

################################################################################
# Prefix the titles of newly created tasks.
#
task_prefix: __DEFAULT_PREFIX
"""
