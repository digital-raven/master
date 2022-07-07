from datetime import date, datetime

from master.util.parse_date import parse_date


class TaskDate:
    """ Special date class used by Task

    Overloads comparison operators so task.*date* attributes will parse
    the strings they get as dates for comparison. This allows tasks to
    compare their *date* fields to strings like "last wednesday" correctly.
    """
    def __init__(self, date_):
        """ date needs to be parseable according to parse_date

        Raises:
            ValueError if the date could not be parsed.
        """
        self.date = parse_date(date_)

    def __str__(self):
        days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        d = self.date
        weekday = days[d.weekday()]

        s = f'{d.year}-{d.month:02d}-{d.day:02d}, {weekday}'

        if type(self.date) is datetime:
            s += f', {d.hour:02d}:{d.minute:02d}'

        return s

    def _compato(self, o):
        """ Return type-compatible versions of self.date and o

        If the types mismatch (datetime / date) then the datetime will be
        tied down to its date elements.
        """
        if type(o) is TaskDate:
            o = o.date
        else:
            o = parse_date(o)

        st = type(self.date)
        ot = type(o)

        if st is ot:
            return self.date, o

        # tie down datetimes to dates
        elif st is datetime and ot is date:
            return self.date.date(), o

        return self.date, o.date()

    def __lt__(self, o):
        s, o = self._compato(o)
        return s < o

    def __gt__(self, o):
        s, o = self._compato(o)
        return s > o

    def __ge__(self, o):
        s, o = self._compato(o)
        return s >= o

    def __le__(self, o):
        s, o = self._compato(o)
        return s <= o

    def __eq__(self, o):
        s, o = self._compato(o)
        return s == o

    def __ne__(self, o):
        s, o = self._compato(o)
        return s != o
