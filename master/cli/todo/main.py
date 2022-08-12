import sys
from datetime import datetime, date

import recurring_ical_events
from icalendar import Calendar

from master.Project import Project
from master.TaskDate import TaskDate
from master.util.parse_date import parse_date


def _trim(s):
    if s.startswith('./'):
        s = s.split('./', 1)[-1]
    return s


def extract_events(cal, start, end):
    """ Return events active between two dates.

    dates are in general, datetimes in specific

    Args:
        start: date or datetime of date to start after
        end: date or datetime of date include before but not inclusive

    Returns:
        tuple of general, specific. Events only specified by their date
        are in general and datetimes are by datetime
    """
    general = []
    specific = []

    for e in recurring_ical_events.of(cal).between(start, end):
        d = e['dtstart'].dt
        if type(d) is date:
            general.append(e)
        elif type(d) is datetime:
            specific.append(e)

    return general, specific


def pretty_output(cal, target_date):
    general, specific = extract_events(
        cal,
        parse_date(target_date),
        parse_date(f'{target_date} + 1 day'))

    general.sort(key=lambda x: x['uid'])
    specific.sort(key=lambda x: x['dtstart'].dt)

    ret = []
    if general or specific:
        ret.append('')
        ret.append('Reminders\n---------')

    if general:
        for e in general:
            ret.append(f'- {_trim(e["UID"])}')
        ret.append('')

    if specific:
        for e in specific:
            start = e['dtstart'].dt
            s = f'- {start.strftime("%H:%M")}'
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

            s += f' {_trim(e["UID"])}'

            ret.append(s)

    return '\n'.join(ret)


def print_remind(cal, target_date):
    """ Print remind-compliant output to stdout

    Designed to piped into remind.
    """
    general, specific = extract_events(
        cal,
        parse_date(target_date),
        parse_date(f'{target_date} + 1 day'))

    for e in general + specific:
        d = e['DTSTART'].dt
        fmt = ''
        if type(d) is date:
            fmt = 'REM %Y-%m-%d'
        else:
            fmt = 'REM %Y-%m-%d %H:%M'
        s = d.strftime(fmt)
        uid = e['UID']

        print(f'{s} {_trim(e["UID"])}')


def print_active(project, date_):
    """ Print events that are still active.

    These are recurring events that are still in circulation or accute
    evnets that haven't happened yet.
    """
    filter_ = (
        f't.event_begin != None and t.event_begin >= "{date_}" '
        f'or t.event_end != None and t.event_end >= "{date_}" '
        f'or t.due_date != None and t.due_date >= "{date_}" '
        f'or t.recurring_stop == None and t.recurring != None '
        f'or t.recurring_stop != None and t.recurring_stop >= "{date_}" ')

    active = []
    for p, root, tasks in project.filteredTasks(filter_, project.path):
        active.extend([f'- {_trim(f"{root}/{t.title}")}' for t in tasks])

    print('\n'.join(active))


def extract_calendar(project, target_date):
    """ Extract an icalendar Calendar from a project.
    """
    cal = Calendar()
    for p, root, tasks in project.filteredTasks('', project.path):
        events = [t.asIcsEvent(f'{root}/{t.title}') for t in tasks]
        [cal.add_component(e) for e in events if e]

    return cal


def do_todo(args):
    """ Look at tasks within a project and print things you should do.
    """
    try:
        project = Project.loadFromDisk(args.project)
    except ValueError as ve:
        print(f'ERROR: {ve}')
        sys.exit(1)

    if project is None:
        print(f'ERROR: "{args.project}" does not host a project.')
        sys.exit(1)

    cal = extract_calendar(project, args.date)
    if args.remind:
        print_remind(cal, args.date)
    elif args.list_active:
        print_active(project, args.date)
    else:
        print(pretty_output(cal, args.date))
