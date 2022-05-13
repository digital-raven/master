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

    query = '"due_date" in t and t.due_date == "today" or "recurring" in t'

    today = parse_date('today')

    cal = Calendar()
    events = []
    for p, root, tasks in project.filteredTasks(query, '.'):
        events = [t.asIcsEvent(f'{root}/{t.title}') for t in tasks]
        [cal.add_component(e) for e in events]

    # TODO: I don't know exactly how to design around ICS events. Maybe
    # this approach should be improved.
    for event in recurring_ical_events.of(cal).at(today):
        print(event['uid'])
