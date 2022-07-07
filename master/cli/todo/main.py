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

    morning = parse_date('today')
    midnight = parse_date('today 11:59pm')

    cal = Calendar()
    events = []
    for p, root, tasks in project.filteredTasks('', '.'):
        events = [t.asIcsEvent(f'{root}/{t.title}') for t in tasks]
        [cal.add_component(e) for e in events if e]

    general = []
    specific = []
    for e in recurring_ical_events.of(cal).between(morning, midnight):
        d = e['dtstart'].dt
        if d.hour == 0 and d.minute == 0:
            general.append(e)
        else:
            specific.append(e)

    general.sort(key=lambda x: x['uid'])
    specific.sort(key=lambda x: x['dtstart'])

    if general:
        print('')
        print('Sometime today\n==============')
        print('\n'.join([e['uid'] for e in general]) + '\n')

    if specific:
        print('But at specific times...\n========================')
        for e in specific:
            start = e['dtstart'].dt
            s = f'{start.hour}:{start.minute}'
            if 'duration' in e:
                td = e['duration'].dt
                days = td.days
                seconds = td.seconds
                hours = int(td.seconds / 3600)
                seconds = max(seconds - hours * 3600, 0)
                minutes = int(seconds / 60)

                s += ' for '
                l_ = []
                if days:
                    l_.append(f'{days} days')
                if hours:
                    l_.append(f'{hours} hours')
                if minutes:
                    l_.append(f'{minutes} minutes')
                s += ' and '.join(l_)

            s += f', {e["uid"]}'

            print(s)
