import re
from datetime import datetime

import parsedatetime as pdt


def parse_date(date):
    """ Generate a more human-readable title.

    Returns:
        A string showing the date in Y-m-d format and the weekday.

    Raises:
        ValueError if date could not be parsed.
    """
    cal = pdt.Calendar(version=pdt.VERSION_CONTEXT_STYLE)
    d, flag = cal.parse(date)

    if not flag:
        raise ValueError('The date "{}" could not be parsed.'.format(date))

    d = datetime(*d[:3])

    days = ['Mon', 'Tues', 'Wed', 'Thurs', 'Fri', 'Sat', 'Sun']

    return '{}-{:02d}-{:02d}, {}'.format(d.year, d.month, d.day, days[d.weekday()])


class Task:
    """ Represents a task.

    Every task, at a minimum, has a title, creator, ID, stage, assignee,
    project name, and tags.
    """
    def __init__(self, title, description, values=None, **kwargs):
        """ Init a new Task.

        Args:
            title: Title of the task.
            description: A longer description about the task.
            values: Metadata about the task. Each task is required to have
                the following values at a minimum.

                assignee: Userid of the person who is assigned the task.
                project: Name of the project which owns the task
                date: String representing the task's creation date. Can be
                    human-readable; like 'today', or 'last wednesday'.
                creator: The userid of the person who created the task.
                stage: What stage the task is in. Defaults to "todo".
                id: The task's ID. It is on the creator to ensure it is unique.
                tags: List of tags for the task.:

                These values may also be provided to the constructor via
                keyword arguments. Tasks may have additional values.

        Raises:
            ValueError if not all required values were provided.
        """
        values = values or dict()

        if 'id' not in values and 'id' not in kwargs:
            raise ValueError('No ID provided.')

        self.title = title
        self.description = description

        # Process values
        self.values = {}
        self.values.update(values)
        self.values.update(kwargs)

        # Set certain defaults
        if 'assignee' not in self.values:
            self.values['assignee'] = ''
        if 'date' not in self.values:
            self.values['date'] = parse_date('today')
        if 'stage' not in self.values:
            self.values['stage'] = 'todo'
        if 'tags' not in self.values:
            self.values['tags'] = []

        self.check()
        self.refresh()

    def refresh(self):
        """ Make minor corrections to values.

        Sort and downcase the tags, alphabetize the keys in values,
        and ensure the title starts with the ID.
        """
        try:
            self.tags = sorted(list(set([x.lower() for x in self.tags])))
        except AttributeError:
            self.values['tags'] = {}

        nv = {k:self.values[k] for k in sorted(self.values)}
        self.values = nv

        # The title should have the ID as a prefix.
        if not self.title.startswith(self.id):
            self.title = f'{self.id}: {self.title}'

    def check(self):
        """ Check the validity of this task's values.

        Will raise an exception if expected keys are missing from the
        metadata, or if the keys aren't valid python3 var names.

        Raises:
            ValueError: The error message will indicate the problem with
                any keys.
        """
        exp = {'assignee', 'creator', 'date', 'id', 'project', 'stage', 'tags'}
        missing = []
        for e in exp:
            if e not in self.values:
                missing.append(e)

        if missing:
            t = self.title
            missing = ', '.join(missing)
            raise ValueError(f'Task "{t}" is missing the {missing} values.')

        # TODO: Python3 supports unicode in var names. Add that here.
        invalid = []
        for k in self.values:
            if not re.search('[a-zA-Z_][a-zA-Z0-9_]*', k):
                invalid.append(k)

        if invalid:
            invalid = ', '.join(invalid)
            raise ValueError('The following keys are invalid: {invalid}')

    @classmethod
    def createFromRst(cls, rst):
        """ Create a new Task from RST text

        The title is expected to be an RST level-1 heading (=====). This
        is followed by the task's description.

        At the end of the description are the values. These are single
        line values which contain metadata about the task.

        The minimum required set for these values are the task's ID,
        date of creation, username of the creator, tags, and assignee.

            ==========================
             PROJ-77: My task's title
            ==========================
            My tasks's description

            Other heading
            -------------
            My other heading description

            creator: ciminobo
            assignee: ciminobo
            date: 05/07/1993
            ...

        Args:
            rst: RST-formatted text from which to create the task. This value
                be provided as a string of RST formatted text, a filename, or
                a list where each value represents a line of RST text.

        Returns:
            A new Task.

        Raises:
            ValueError: If the RST could not create a valid Task.
        """
        if type(rst) is str:
            rst = rst.strip().splitlines()
            if len(rst) == 1:
                with open(rst[0]) as f:
                    rst = f.read().strip().splitlines()

        if not rst:
            raise ValueError('The task was empty.')

        ptr = 0

        values = {}

        # Extract the values first. Some may be modified in special ways.
        curline = rst[-1].strip()
        while curline != '':
            curline = curline.split(':')
            key, value = curline[0], ':'.join(curline[1:]).strip()

            # Store tags as a list
            if key == 'tags':
                value = value.replace(',', ' ').replace(':', ' ').split()
                value = sorted(list(set(value)))
            elif 'date' in key or 'time' in key:  # Try to parse dates
                value = parse_date(value)

            values[key] = value
            rst = rst[:-1]
            curline = rst[-1].strip()

        # Find the title.
        if re.search('^=+$', rst[0].strip()):
            rst = rst[1:]

        title = rst[0].strip()

        # Chop off the title block and build the description
        if re.search('^=+$', rst[1].strip()):
            rst = rst[2:]
        description = '\n'.join(rst).strip()

        return Task(title, description, values)

    def update(self, new_task):
        """ Update a task.

        The title and description of this task will be replaced, and the
        values will be replaced with the values in the new task.

        Designed to replace an existing task with the one modified in
        a text editor.

        Args:
            new_task: Other task instance whose values will be used.

        Raises:
            See createFromRst.
        """
        self.title = new_task.title
        self.description = new_task.description
        self.values = new_task.values

        self.check()
        self.refresh()

    def getRst(self):
        """ Display this task in RST format.

        Returns:
            An RST string representing the content of this task.
        """
        s = []
        s.append('=' * (len(self.title) + 2))
        s.append(' ' + self.title)
        s.append(s[0])

        s.append(self.description)
        s.append('')

        # Add the values alphabetically
        for k in sorted(self.values.keys()):
            v = self.values[k]
            if k == 'tags':
                v = ', '.join(v)

            s.append(f'{k}: {v}')

        # Will become trailing newline
        s.append('')

        return '\n'.join(s)

    def __getattr__(self, key):
        """ Expose keys in values as attributes.
        """
        if key in self.__dict__:
            return self.__dict__[key]
        else:
            try:
                return self.values[key]
            except KeyError as e:
                raise AttributeError(f"'Task' object has no attribute {key}")
