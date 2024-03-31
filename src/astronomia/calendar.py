"""Copyright 2000, 2001 Astrolabe by William McClain.

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

A collection of date and time functions.

The functions which use Julian Day Numbers are valid only for positive values,
i.e., for dates after -4712 (4713BC).

Unless otherwise specified, Julian Day Numbers may be fractional values.

Numeric years use the astronomical convention of a year 0: 0 = 1BC, -1 = 2BC,
etc.

Numeric months are 1-based: Jan = 1...Dec = 12.

Numeric days are the same as the calendar value.

Reference: Jean Meeus, *Astronomical Algorithms*, second edition, 1998,
Willmann-Bell, Inc.
"""

import datetime
import time
from math import modf

import numpy as np

from astronomia import globals as globls
from astronomia.constants import minutes_per_day, seconds_per_day
from astronomia.util import _scalar_if_one, d_to_r, modpi2


class Error(Exception):
    """local exception class."""


def frac_yr_to_jd(year, gregorian=True):
    """Convert a date in the Julian or Gregorian fractional year to the Julian
    Day Number (Meeus 7.1).

    Arguments:
      - `year` : (int, float)  year

    Keywords:
      - `gregorian` : (bool, default=True) If True, use Gregorian calendar,
        else use Julian calendar

    Returns:
      - (float)
    """
    year = np.atleast_1d(year)
    day = np.atleast_1d(0.0).astype(np.float64)
    year, day = list(map(np.array, np.broadcast_arrays(year, day)))
    # For float years abuse the day variable
    fyear = year - year.astype("i")
    mask = fyear > 0
    if np.any(mask):
        year = year.astype("i")
        days_in_year = cal_to_jd(year[mask] + 1) - cal_to_jd(year[mask])
        day[mask] = days_in_year * fyear[mask]
        return _scalar_if_one(cal_to_jd(year) + day)
    return _scalar_if_one(cal_to_jd(year))


def yr_frac_mon_to_jd(year, mon, gregorian=True):
    """Convert a year and fractional month in the Julian or Gregorian calendars
    to the Julian Day Number (Meeus 7.1).

    Arguments:
      - `year` : (int)  year
      - `mon` : (int, float)  month

    Keywords:
      - `gregorian` : (bool, default=True) If True, use Gregorian calendar,
        else use Julian calendar

    Returns:
      - (float)
    """
    year = np.atleast_1d(year)
    mon = np.atleast_1d(mon).astype(np.float64)
    day = np.atleast_1d(0.0).astype(np.float64)
    year, mon, day = list(map(np.array, np.broadcast_arrays(year, mon, day)))
    fmon = mon - mon.astype("i")
    mask = fmon > 0
    if np.any(mask):
        mon = mon.astype("i")
        next_mon = np.copy(mon) + 1
        next_year = np.copy(year)
        next_mon_mask = next_mon == 13
        next_year[next_mon_mask] = next_year[next_mon_mask] + 1
        next_mon[next_mon_mask] = 1
        days_in_mon = cal_to_jd(next_year[mask], next_mon[mask]) - cal_to_jd(
            year[mask], mon[mask]
        )
        day[mask] = days_in_mon * fmon[mask]
        return _scalar_if_one(cal_to_jd(year, mon) + day)
    return _scalar_if_one(cal_to_jd(year, mon))


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
    year = np.atleast_1d(year)
    mon = np.atleast_1d(mon)
    day = np.atleast_1d(day).astype(np.float64)

    mask = _extracted_from_cal_to_jd_21(
        year, "Year must be integer. Use frac_yr_to_jd instead."
    )
    mask = _extracted_from_cal_to_jd_21(
        mon, "Month must be integer. Use yr_frac_mon_to_jd instead."
    )
    if np.any(mon > 12) or np.any(mon < 1):
        raise ValueError("Month must be from 1 to 12")
    if np.any(day > 31) or np.any(day < 1):
        raise ValueError("Day must be from 1 to 31")
    year, mon, day = list(map(np.array, np.broadcast_arrays(year, mon, day)))

    for thirtydays in (9, 4, 6, 11):
        daytestarr = mon == thirtydays
        if np.any(day[daytestarr] > 30):
            raise ValueError("Day must be from 1 to 30")

    leapyeartest = np.atleast_1d(is_leap_year(year, gregorian))

    if np.any(np.logical_and(day[leapyeartest] > 29, mon[leapyeartest] == 2)):
        raise ValueError("Day must be from 1 to 29")
    if np.any(np.logical_and(day[~leapyeartest] > 28, mon[~leapyeartest] == 2)):
        raise ValueError("Day must be from 1 to 28")

    testarr = mon <= 2
    year[testarr] -= 1
    mon[testarr] += 12
    if gregorian:
        A = (year / 100).astype(np.int64)
        B = 2 - A + (A / 4).astype(np.int64)
    else:
        B = 0
    return _scalar_if_one(
        (365.25 * (year + 4716)).astype(np.int64)
        + (30.6001 * (mon + 1)).astype(np.int64)
        + day
        + B
        - 1524.5
    )


# TODO Rename this here and in `cal_to_jd`
def _extracted_from_cal_to_jd_21(arg0, arg1):
    fyear = arg0 - arg0.astype("i")
    result = fyear > 0
    if np.any(result):
        raise ValueError(arg1)
    return result


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
    julian_day = np.atleast_1d(julian_day)
    F, Z = np.modf(julian_day + 0.5)
    if gregorian:
        alpha = ((Z - 1867216.25) / 36524.25).astype(np.int64)
        A = Z + 1 + alpha - (alpha / 4).astype(np.int64)
    else:
        A = Z
    B = A + 1524
    C = ((B - 122.1) / 365.25).astype(np.int64)
    D = (365.25 * C).astype(np.int64)
    E = ((B - D) / 30.6001).astype(np.int64)
    day = B - D - (30.6001 * E).astype(np.int64) + F
    mon = E - 13
    mon[E < 14] = E[E < 14] - 1
    year = C - 4715
    year[mon > 2] = C[mon > 2] - 4716
    return _scalar_if_one(year), _scalar_if_one(mon), _scalar_if_one(day)


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
    return _scalar_if_one(jde + hms_to_fday(hour, minute, sec))


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
    year = np.atleast_1d(year).astype(np.int64)
    mon = np.atleast_1d(mon).astype(np.int64)
    day = np.atleast_1d(day).astype(np.int64)
    year, mon, day = np.broadcast_arrays(year, mon, day)
    K = np.ones_like(year)
    K[:] = 2
    K[np.atleast_1d(is_leap_year(year, gregorian))] = 1
    return _scalar_if_one(
        (275 * mon / 9.0).astype(np.int64)
        - (K * ((mon + 9) / 12.0).astype(np.int64))
        + day
        - 30
    )


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
    year = np.atleast_1d(year)
    N = np.atleast_1d(N)
    year, N = np.broadcast_arrays(year, N)
    K = np.ones_like(N)
    K[:] = 2
    K[np.atleast_1d(is_leap_year(year, gregorian))] = 1
    mon = (9 * (K + N) / 275.0 + 0.98).astype(np.int64)
    mon[N < 32] = 1
    day = (
        N
        - (275 * mon / 9.0).astype(np.int64)
        + K * ((mon + 9) / 12.0).astype(np.int64)
        + 30
    ).astype(np.int64)
    return _scalar_if_one(mon), _scalar_if_one(day)


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
    year = np.atleast_1d(year)
    if gregorian:
        tmp = _extracted_from_easter_17(year)
    else:
        tmp = _extracted_from_easter_31(year)
    mon = tmp // 31
    day = (tmp % 31) + 1
    return _scalar_if_one(mon), _scalar_if_one(day)


# TODO Rename this here and in `easter`
def _extracted_from_easter_31(year):
    a = year % 4
    b = year % 7
    c = year % 19
    d = (19 * c + 15) % 30
    e = (2 * a + 4 * b - d + 34) % 7
    return d + e + 114


# TODO Rename this here and in `easter`
def _extracted_from_easter_17(year):
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
    return h + l - 7 * m + 114


def fday_to_hms(day):
    """Convert fractional day (0.0..1.0) to integral hours, minutes, seconds.

    Arguments:
      - day : a fractional day in the range 0.0..1.0

    Returns:
      - hour : (int, 0..23)
      - minute : (int, 0..59)
      - second : (int, 0..59)
    """
    # First get rid of the integer day
    fday, days = modf(day)
    seconds = fday * 86400.0
    minutes = int(seconds / 60.0)
    seconds = seconds - (minutes * 60.0)
    hours = int(minutes / 60.0)
    minutes -= hours * 60.0
    return hours, minutes, int(seconds)


def hms_to_fday(hr, mn, sec):
    """Convert hours-minutes-seconds into a fractional day 0.0..1.0.

    Arguments:
      - `hr` : hours, 0..23
      - `mn` : minutes, 0..59
      - `sec` : seconds, 0..59

    Returns:
      - fractional day, 0.0..1.0
    """
    hr = np.atleast_1d(hr)
    mn = np.atleast_1d(mn)
    sec = np.atleast_1d(sec)
    hr, mn, sec = np.broadcast_arrays(hr, mn, sec)
    return (hr / 24.0) + (mn / minutes_per_day) + (sec / seconds_per_day)


def is_dst(julian_day):
    """Is this instant within the Daylight Savings Time period.

    Uses the time zone database associated with Python and used in the 'time'
    module.

    Arguments:
      - `julian_day` : (int) Julian Day number representing an instant in
        Universal Time

    Returns:
      - (bool) True if Daylight Savings Time is in effect, False otherwise.
    """
    year, mon, day = jd_to_cal(julian_day)
    day = int(day)
    hr, minute, second = fday_to_hms(julian_day)
    second = int(second)

    stamp = datetime.datetime(year, mon, day, hr, minute, second)
    return time.localtime(time.mktime(stamp.timetuple())).tm_isdst == 1


def is_leap_year(year, gregorian=True):
    """Return True if this is a leap year in the Julian or Gregorian calendars.

    Arguments:
      - `year` : (int) year

    Keywords:
      - `gregorian` : (bool, default=True) If True, use Gregorian calendar,
        else use Julian calendar

    Returns:
      - (bool) True is this is a leap year, else False.
    """
    year = np.atleast_1d(year).astype(np.int64)
    x = np.fmod(year, 4)
    if gregorian:
        x = np.fmod(year, 4)
        y = np.fmod(year, 100)
        z = np.fmod(year, 400)
        return _scalar_if_one(
            np.logical_and(np.logical_not(x), np.logical_or(y, np.logical_not(z)))
        )
    return _scalar_if_one(x == 0)


def jd_to_day_of_week(julian_day):
    """Return the day of week for a Julian Day Number.

    The Julian Day Number must be for 0h UT.

    Arguments:
      - `julian_day` : (int) Julian Day number

    Returns:
      - day of week : (int) 0 = Sunday...6 = Saturday.
    """
    julian_day = np.atleast_1d(julian_day)
    i = (julian_day + 1.5).astype(np.int64)
    return _scalar_if_one(i % 7)


def jd_to_jcent(julian_day):
    """Return the number of Julian centuries since J2000.0.

    Arguments:
      - `julian_day` : (int) Julian Day number

    Return:
      - Julian centuries : (int)
    """
    julian_day = np.atleast_1d(julian_day)
    return _scalar_if_one((julian_day - 2451545.0) / 36525.0)


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

    if level == "second":
        return f"{year}-{mon:02}-{iday:02} {hour:02}:{minute:02}:{sec:02} {zone}"
    if level == "minute":
        return f"{year}-{mon:02}-{iday:02} {hour:02}:{minute:02} {zone}"
    if level == "hour":
        return f"{year}-{mon:02}-{iday:02} {hour:02} {zone}"
    if level == "day":
        return f"{year}-{mon:02}-{iday:02}"

    raise Error(f"unknown time level = {level}")


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
    theta0 = (
        280.46061837
        + 360.98564736629 * (julian_day - 2451545.0)
        + 0.000387933 * T2
        - T3 / 38710000
    )
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
        zone = globls.daylight_timezone_name
        offset = globls.daylight_timezone_offset
    else:
        zone = globls.standard_timezone_name
        offset = globls.standard_timezone_offset

    julian_day = julian_day - offset
    return julian_day, zone
