from datetime import datetime as dt

import recurring_ical_events
from icalendar import Calendar

from master.Project import Project
from master.Task import parse_date


def do_todo(args):
    """ Look at tasks within a project and print things you should do today.

    Generate an ICS file using events that are due today or have a "recurring"
    attribute, and then iterate over the ICS file to print titles of tasks.
    """
    project = Project.loadFromDisk('./')

    today = parse_date('today')

    cal = Calendar()
    events = []
    for p, root, tasks in project.filteredTasks('', '.'):
        events = [t.asIcsEvent(f'{root}/{t.title}') for t in tasks]
        [cal.add_component(e) for e in events if e]

    for event in recurring_ical_events.of(cal).at(today):
        print(event['uid'])
