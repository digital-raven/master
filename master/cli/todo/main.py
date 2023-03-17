import sys
from datetime import datetime, date

from superdate import parse_date
from libzet import load_zettels

import recurring_ical_events
from icalendar import Calendar


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
        ret.append('Todo\n----')

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


def print_active(zettels, date_):
    """ Print events that are still active.

    These are recurring events that are still in circulation or accute
    evnets that haven't happened yet.
    """
    def filter_(t):
        return (t.attrs["event_begin"] != None and t.attrs["event_begin"] >= date_
            or t.attrs["event_end"] != None and t.attrs["event_end"] >= date_
            or t.attrs["due_date"] != None and t.attrs["due_date"] >= date_
            or t.attrs["recurring_stop"] == None and t.attrs["recurring"] != None
            or t.attrs["recurring_stop"] != None and t.attrs["recurring_stop"] >= date_)

    active = []
    for z in filter(filter_, zettels):
        line = _trim(f'{z.attrs["_loadpath"]}: {z.title}')
        active.append(f'- {line}')

    print('\n'.join(active))


def extract_calendar(zettels, target_date):
    """ Get an icalendar Calendar from a list oz zettels.
    """
    cal = Calendar()
    events = [t.asIcsEvent(t.title) for t in zettels]
    [cal.add_component(e) for e in events if e]

    return cal


def do_todo(args):
    """ Look at tasks within a project and print things you should do.
    """
    zettels = load_zettels(args.zettels, recurse=True)
    cal = extract_calendar(zettels, args.date)
    if args.remind:
        print_remind(cal, args.date)
    elif args.list_active:
        print_active(zettels, args.date)
    else:
        print(pretty_output(cal, args.date))
