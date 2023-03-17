task = """\
################################################################################
# This is a configuration for projects with basic tasks. The settings
# in this file will be copied to new projects as project.yaml
#
# Settings in this string that begin with a double underscore are automatically
# replaced when the real project configuration is created.
#

# Default zettel format. md or rst
zettel_format: md

# Default headings for new tasks
headings: []

################################################################################
# A basic task adds a due_date, stage, and project name. The only stage value
# reserved by master is "closed". "closed" tasks are omitted from master
# filters by default. Feel free to use any other values as your own.
#
attrs:
  due_date:
  project: __DEFAULT_PROJECT_NAME
  stage: todo

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
