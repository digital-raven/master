import re
import yaml

from icalendar import Event

from master.Attributes import Attributes
from master.TaskDate import TaskDate
from master.util.parse_date import parse_date, parse_duration
from master.util.NoCompare import NoCompare


def parse_rrule(rrule):
    """ Parse an icalendar rrule str into a dict.

    Follow the ICS convention for rrules.

    https://icalendar.org/iCalendar-RFC-5545/3-8-5-3-recurrence-rule.html

    But omit the leading "RRULE:".

    Use the return of this function like this.

        event['rrule'] = parse_rrule(some_rrule))

    Arg:
        rrule: The str rrule to parse.

    Returns:
        An rrule object that can be directly set as an icalendar.Event's
        'rrule' index.

    Raises:
        ValueError if the rrule str wasn't valid.
    """
    rrule = 'RRULE:' + rrule
    s = '\n'.join(['BEGIN:VEVENT', rrule, 'END:VEVENT'])
    event = Event.from_ical(s)

    if not len(event['rrule']):
        raise ValueError('Invalid rrule')

    return event['rrule']


class Task:
    """ Represents a task.

    Every task, at a minimum, has a title, creator, ID, stage, assignee,
    project name, and tags.
    """
    def __init__(self, title, description, attributes=None, **kwargs):
        """ Init a new Task.

        Args:
            title: Title of the task.
            description: A longer description about the task.
            attributes: Metadata about the task. Each task is required to have
                the following attributes at a minimum.

                creation_date: String representing the task's creation date.
                    Can be human-readable; like 'today', or 'last wednesday'.
                creator: The userid of the person who created the task.
                id: The task's ID. It is on the creator to ensure it is unique.
                project: Name of the project which owns the task
                stage: What stage the task is in. Defaults to "todo".
                tags: List of tags for the task.

                These attributes may also be provided to the constructor via
                keyword arguments. Tasks may have additional attributes.

        Raises:
            ValueError if some attribute keys were invalid.
        """
        attributes = attributes or dict()

        self.title = title
        self.description = description

        # Process attributes
        self.attributes = Attributes()
        self.attributes.update(attributes)
        self.attributes.update(kwargs)

    def asIcsEvent(self, uid):
        """ Return an icalendar.Event class from this Task's data.

        A task must have either a event_begin or a due_date to be
        considered capable of turning into an ICS Event.

        This function does not support all ICS Event values. The
        supported values are...
        - uid
        - dtstamp: Initialized to the time this method was called.
        - summary
        - description
        - dtstart: as event_begin or due_date with respective *_time's
        - dtend: as event_end + end_time (optional)
        - rrule: as recurring

        Returns:
            An icalendar.Event created from this instance's data. If
            this task doesn't have a due_date or event_begin field then
            None will be returned.
        """
        exp = ['event_begin', 'due_date']
        if not any([x in self.attributes and self.attributes[x] for x in exp]):
            return None

        event = Event()
        event.add('uid', uid)
        event.add('summary', self.title)
        event.add('description', self.description)

        event.add('dtstamp', parse_date('today'))

        if 'event_begin' in self and self.event_begin:
            event.add('dtstart', self.event_begin.date)
        elif 'due_date' in self and self.due_date:
            event.add('dtstart', self.due_date.date)

        # recurring tasks should also have event_begin
        if 'recurring' in self and self.recurring:
            rrule = self.recurring

            if 'recurring_stop' in self and self.recurring_stop:
                rrule += f';until={self.recurring_stop.asRrule()}'

            event['rrule'] = parse_rrule(rrule)

        # Add duration.
        if 'duration' in self and self.duration:
            event.add('duration', parse_duration(self.duration))

        # Parse dtend
        if 'event_end' in self and self.event_end:
            event.add('dtend', self.event_end.date)

        return event

    @classmethod
    def createFromRst(cls, rst):
        """ Create a new Task from RST text

        The title is expected to be an RST level-1 heading (=====). This
        is followed by the task's description.

        At the end of the description are the attributes. These are single
        line attributes which contain metadata about the task.

        The minimum required set for these attributes are the task's ID,
        date of creation, username of the creator, tags, and assignee.

            ==========================
             PROJ-77: My task's title
            ==========================
            My tasks's description

            Other heading
            -------------
            My other heading description

            .. attributes
            creator: ciminobo
            assignee: ciminobo
            creation_date: 05/07/1993
            .. attributes

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

        # Extract the attributes first. These are expected at the bottom.
        idx = rst.index('.. attributes')
        attributes = yaml.safe_load('\n'.join(rst[idx+1:-1]))
        rst = rst[:idx]

        # Find the title.
        if re.search('^=+$', rst[0].strip()):
            rst = rst[1:]

        title = rst[0].strip()

        # Chop off the title block and build the description
        if re.search('^=+$', rst[1].strip()):
            rst = rst[2:]
        description = '\n'.join(rst).strip()

        return Task(title, description, attributes)

    def update(self, new_task):
        """ Update a task.

        The title and description of this task will be replaced, and the
        attributes will be replaced with the attributes in the new task.

        Designed to replace an existing task with the one modified in
        a text editor.

        Args:
            new_task: Other task instance whose attributes will be used.

        Raises:
            See createFromRst.
        """
        self.title = new_task.title
        self.description = new_task.description
        self.attributes = Attribtes()
        self.attributes.update(new_task.attributes)

    def getRst(self):
        """ Display this task in RST format.

        Returns:
            An RST string representing the content of this task.
        """
        thead = '=' * (len(self.title) + 2)
        s = [
            thead,
            ' ' + self.title,
            thead,
            self.description,
            '',
            '.. attributes',
            yaml.dump(self.attributes.toYamlDict()),
            '.. attributes',
            '',
        ]

        return '\n'.join(s)

    def __eq__(self, o):
        """ Returns true if o.title matches this one.
        """
        return self.title == o.title

    def __lt__(self, o):
        """ Returns true if o.title is less than this one.
        """
        return self.title < o.title

    def __getattr__(self, key):
        """ Expose keys in self.attributes as attributes.
        """
        if key in self.__dict__:
            return self.__dict__[key]

        return self.attributes[key]

    def __contains__(self, key):
        """ Return True if key is in the Task's dict or attributes.
        """
        if key in self.__dict__:
            return True

        return key in self.attributes
