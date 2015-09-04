import re
import datetime
import dateutil.parser


class RFC3339(object):
    date = re.compile("^[0-9]{4}-(0[1-9]|1[012])-(0[1-9]|[12][0-9]|3[01])$")  # <AAAA>-<MM>-<DD>
    time = re.compile("^(0[0-9]|1[0-9]|2[0-3]):([0-5][0-9])(:(([0-5][0-9])|60))?(.[1-9]+)?$")  # <HH>:<MM>[:<SS>[.<XXXX>]]
    datetime = re.compile("^[0-9]{4}-(0[1-9]|1[012])-(0[1-9]|[12][0-9]|3[01])(t|T)(0[0-9]|1[0-9]|2[0-3]):([0-5][0-9])(:(([0-5][0-9])|60))?(.[1-9]+)?(Z|((\+|-)(0[0-9]|1[0-9]|2[0-3])):([0-5][0-9]))$")  # <AAAA>-<MM>-<DD>T<HH>:<MM>[:<SS>[.<XXXX>]](Z|((+|-)<HH>:<MM>))


class Rfc3339(object):
    """ Tools compliant with :rfc:`3339` to play with dates and times."""
    @staticmethod
    def parse(string):
        """
        Convert a date, datetime or time from string to python object.

        :param str string: A string in :rfc:`3339` format.
        :rtype: :py:class:`datetime.date`, :py:class:`datetime.datetime` or :py:class:`datetime.time`.
        """
        try:
            if RFC3339.date.match(string):
                return datetime.datetime.strptime(string, "%Y-%m-%d").date()
            elif RFC3339.datetime.match(string):
                return dateutil.parser.parse(string).astimezone(dateutil.tz.tzutc())
            elif RFC3339.time.match(string):
                return dateutil.parser.parse(string).time()
        except:
            pass
        return string

    @staticmethod
    def reverse(date):
        if type(date) is datetime.date:
            return date.strftime('%Y-%m-%d')
        elif type(date) is datetime.time:
            return date.strftime('%H:%M:%S')
        elif type(date) is datetime.datetime:
            return date.strftime('%Y-%m-%d %H:%M:%S')
        else:
            return str(date)
