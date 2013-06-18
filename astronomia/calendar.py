
from __future__ import division

"""
    Copyright 2000, 2001 Astrolabe by William McClain
    Forked in 2013 to Astronomia
    Copyright 2013 Astronomia by Tim Cera

    This file is part of Astronomia.

    Astronomia is free software; you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation; either version 2 of the License, or
    (at your option) any later version.

    Astronomia is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with Astronomia; if not, write to the Free Software
    Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
    """

"""A collection of date and time functions.

The functions which use Julian Day Numbers are valid only for positive values,
i.e., for dates after -4712 (4713BC).

Unless otherwise specified, Julian Day Numbers may be fractional values.

Numeric years use the astronomical convention of a year 0: 0 = 1BC, -1 = 2BC,
etc.

Numeric months are 1-based: Jan = 1...Dec = 12.

Numeric days are the same as the calendar value.

Reference: Jean Meeus, _Astronomical Algorithms_, second edition, 1998,
Willmann-Bell, Inc.
"""

from math import modf
from astronomia.util import d_to_r, modpi2, fday_to_hms, hms_to_fday

import astronomia.globals


class Error(Exception):
    """local exception class"""
    pass


def cal_to_jd(year, mon=1, day=1, gregorian=True):
    """Convert a date in the Julian or Gregorian calendars to the Julian Day
    Number (Meeus 7.1).

    Arguments:
      - `year` : (int)  year

    Keywords:
      - `mon`       : (int, default=1) month
      - `day`       : (int, float, default=1) day, may be fractional day
      - `gregorian` : (bool, default=True) If True, use Gregorian calendar,
        else use Julian calendar

    Returns:
      - (int, float)

    """
    if mon <= 2:
        year -= 1
        mon += 12
    if gregorian:
        A = int(year / 100)
        B = 2 - A + int(A / 4)
    else:
        B = 0
    return int(365.25*(year + 4716)) + int(30.6001*(mon + 1)) + day + B - 1524.5


def cal_to_jde(year, mon=1, day=1, hour=0, minute=0, sec=0.0, gregorian=True):
    """Convert a date in the Julian or Gregorian calendars to the Julian Day
    Ephemeris (Meeus 22.1).

    Arguments:
      - `year` : year

    Keywords:
      - `mon`       : (int, default=1) month
      - `day`       : (int, default=1) day, may be fractional day
      - `hour`      : (int, default=0) hour
      - `minute`    : (int, default=0) minute
      - `sec`       : (float, default=0.0) second
      - `gregorian` : (bool, default=True) If True, use Gregorian calendar,
        else use Julian calendar

    Returns:
      - julian day ephemeris : (float)

    """
    jde = cal_to_jd(year, mon, day, gregorian)
    return jde + hms_to_fday(hour, minute, sec)


def cal_to_day_of_year(year, mon, day, gregorian=True):
    """Convert a date in the Julian or Gregorian calendars to day of the year
    (Meeus 7.1).

    Arguments:
      - `year` : (int) year
      - `mon`  : (int) month
      - `day`  : (int) day

    Keywords:
      - `gregorian` : (bool, default=True) If True, use Gregorian calendar,
        else use Julian calendar

    Return:
      - day number : 1 = Jan 1...365 (or 366 for leap years) = Dec 31.

    """
    if is_leap_year(year, gregorian):
        K = 1
    else:
        K = 2
    day = int(day)
    return int(275 * mon / 9.0) - (K * int((mon + 9) / 12.0)) + day - 30


def day_of_year_to_cal(year, N, gregorian=True):
    """Convert a day of year number to a month and day in the Julian or
    Gregorian calendars.

    Arguments:
      - `year`      : year
      - `N`         : day of year, 1..365 (or 366 for leap years)

    Keywords:
      - `gregorian` : If True, use Gregorian calendar, else use Julian calendar
        (default: True)

    Return:
      - (month, day) : (tuple)

    """
    if is_leap_year(year, gregorian):
        K = 1
    else:
        K = 2
    if (N < 32):
        mon = 1
    else:
        mon = int(9 * (K+N) / 275.0 + 0.98)
    day = int(N - int(275 * mon / 9.0) + K * int((mon + 9) / 12.0) + 30)
    return mon, day


def easter(year, gregorian=True):
    """Return the date of Western ecclesiastical Easter for a year in the
    Julian or Gregorian calendars.

    Arguments:
      - `year` : (int) year

    Keywords:
      - `gregorian` : (bool, default=True) If True, use Gregorian calendar,
        else use Julian calendar

    Return:
      - (month, day) : (tuple)

    """
    year = int(year)
    if gregorian:
        a = year % 19
        b = year // 100
        c = year % 100
        d = b // 4
        e = b % 4
        f = (b + 8) // 25
        g = (b - f + 1) // 3
        h = (19 * a + b - d - g + 15) % 30
        i = c // 4
        k = c % 4
        l = (32 + 2 * e + 2 * i - h - k) % 7
        m = (a + 11 * h + 22 * l) // 451
        tmp = h + l - 7 * m + 114
    else:
        a = year % 4
        b = year % 7
        c = year % 19
        d = (19 * c + 15) % 30
        e = (2 * a + 4 * b - d + 34) % 7
        tmp = d + e + 114
    mon = tmp // 31
    day = (tmp % 31) + 1
    return mon, day


def is_dst(julian_day):
    """Is this instant within the Daylight Savings Time period as used in the
    US?

    If astronomia.globals.daylight_timezone_name is None, the function always
    returns False.

    Arguments:
      - `julian_day` : (int) Julian Day number representing an instant in
        Universal Time

    Returns:
      - (bool) True if Daylight Savings Time is in effect, False otherwise.

    """
    if not astronomia.globals.daylight_timezone_name:
        return False

    #
    # What year is this?
    #
    year, mon, day = jd_to_cal(julian_day)
    #
    # First day in April
    #
    start = cal_to_jd(year, 4, 1)

    #
    # Advance to the first Sunday
    #
    dow = jd_to_day_of_week(start)
    if dow:
        start += 7 - dow

    #
    # Advance to 2AM
    #
    start += 2.0 / 24

    #
    # Convert to Universal Time
    #
    start += astronomia.globals.standard_timezone_offset

    if julian_day < start:
        return False

    #
    # Last day in October
    #
    stop = cal_to_jd(year, 10, 31)

    #
    # Backup to the last Sunday
    #
    dow = jd_to_day_of_week(stop)
    stop -= dow

    #
    # Advance to 2AM
    #
    stop += 2.0 / 24

    #
    # Convert to Universal Time
    #
    stop += astronomia.globals.daylight_timezone_offset

    if julian_day < stop:
        return True

    return False


def is_leap_year(year, gregorian=True):
    """Return True if this is a leap year in the Julian or Gregorian calendars

    Arguments:
      - `year` : (int) year

    Keywords:
      - `gregorian` : (bool, default=True) If True, use Gregorian calendar,
        else use Julian calendar

    Returns:
      - (bool) True is this is a leap year, else False.

    """
    year = int(year)
    if gregorian:
        return (year % 4 == 0) and ((year % 100 != 0) or (year % 400 == 0))
    else:
        return year % 4 == 0


def jd_to_cal(julian_day, gregorian=True):
    """Convert a Julian day number to a date in the Julian or Gregorian
    calendars.

    Arguments:
      - `julian_day` : (int) Julian Day Number

    Keywords:
      - `gregorian` : (bool, default=True) If True, use Gregorian calendar,
        else use Julian calendar

    Return:
      - (year, month, day) : (tuple) day may be fractional

    """
    F, Z = modf(julian_day + 0.5)
    if gregorian:
        alpha = int((Z - 1867216.25) / 36524.25)
        A = Z + 1 + alpha - int(alpha / 4)
    else:
        A = Z
    B = A + 1524
    C = int((B - 122.1) / 365.25)
    D = int(365.25 * C)
    E = int((B - D) / 30.6001)
    day = B - D - int(30.6001 * E) + F
    if E < 14:
        mon = E - 1
    else:
        mon = E - 13
    if mon > 2:
        year = C - 4716
    else:
        year = C - 4715
    return year, mon, day


def jd_to_day_of_week(julian_day):
    """Return the day of week for a Julian Day Number.

    The Julian Day Number must be for 0h UT.

    Arguments:
      - `julian_day` : (int) Julian Day number

    Returns:
      - day of week : (int) 0 = Sunday...6 = Saturday.

    """
    i = julian_day + 1.5
    return int(i) % 7


def jd_to_jcent(julian_day):
    """Return the number of Julian centuries since J2000.0

    Arguments:
      - `julian_day` : (int) Julian Day number

    Return:
      - Julian centuries : (int)

    """
    return (julian_day - 2451545.0) / 36525.0


def lt_to_str(julian_day, zone="", level="second"):
    """Convert local time in Julian Days to a formatted string.

    The general format is:

        YYYY-MMM-DD HH:MM:SS ZZZ

    Truncate the time value to seconds, minutes, hours or days as
    indicated. If level = "day", don't print the time zone string.

    Pass an empty string ("", the default) for zone if you want to do
    your own zone formatting in the calling module.

    Arguments:
      - `julian_day` : (int) Julian Day number

    Keywords:
      - `zone`  : (str, default="") Time zone string
      - level : (str, default="second") {"day", "hour", "minute", "second"}

    Return:
      - formatted date/time string : (str)

    """
    year, mon, day = jd_to_cal(julian_day)
    fday, iday = modf(day)
    iday = int(iday)
    hour, minute, sec = fday_to_hms(fday)
    sec = int(sec)

    month = astronomia.globals.month_names[mon-1]

    if level == "second":
        return "%d-%s-%02d %02d:%02d:%02d %s" % (year, month, iday,
                                                 hour, minute, sec, zone)
    if level == "minute":
        return "%d-%s-%02d %02d:%02d %s" % (year, month, iday,
                                            hour, minute, zone)
    if level == "hour":
        return "%d-%s-%02d %02d %s" % (year, month, iday, hour, zone)
    if level == "day":
        return "%d-%s-%02d" % (year, astronomia.globals.month_names[mon-1],
                               iday)
    raise Error("unknown time level = " + level)


def sidereal_time_greenwich(julian_day):
    """Return the mean sidereal time at Greenwich.

    The Julian Day number must represent Universal Time.

    Arguments:
      - `julian_day` : (int) Julian Day number

    Returns:
      - sidereal time in radians : (float) 2pi radians = 24 hours

    """
    T = jd_to_jcent(julian_day)
    T2 = T * T
    T3 = T2 * T
    theta0 = 280.46061837 + \
        360.98564736629*(julian_day - 2451545.0) + \
        0.000387933*T2 - \
        T3/38710000
    result = d_to_r(theta0)
    return modpi2(result)


def ut_to_lt(julian_day):
    """Convert universal time in Julian Days to a local time.

    Include Daylight Savings Time offset, if any.

    Arguments:
      - `julian_day` : (int) Julian Day number, universal time

    Return:
      - Julian Day number : (str) local time
        zone string of the zone used for the conversion

    """
    if is_dst(julian_day):
        zone = astronomia.globals.daylight_timezone_name
        offset = astronomia.globals.daylight_timezone_offset
    else:
        zone = astronomia.globals.standard_timezone_name
        offset = astronomia.globals.standard_timezone_offset

    julian_day = julian_day - offset
    return julian_day, zone
