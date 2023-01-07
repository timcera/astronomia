import os
import sys

import cltoolbox
import pandas as pd
from cltoolbox.rst_text_formatter import RSTHelpFormatter
from toolbox_utils import tsutils

from .calendar import cal_to_jd
from .constants import days_per_second
from .coordinates import ecl_to_equ
from .lunar import Lunar
from .nutation import nutation_in_longitude, nutation_in_obliquity, obliquity
from .planets import geocentric_planet, vsop_to_fk5
from .sun import Sun, aberration_low

moon = Lunar()
sun = Sun()


@cltoolbox.command(formatter_class=RSTHelpFormatter)
def right_ascension(
    latitude, longitude, body, input_ts=None, start_date=None, end_date=None, freq=None
):
    """Print out right ascension.

    :param latitude <float>: The latitude of the location where you want to
        calculate right ascension.
    :param longitude <float>: The longitude of the location where you want to
        calculate right ascension.
    :param body <str>:  Celestial body, one of ['sun', 'moon',
        'mercury', 'venus', 'mars', 'jupiter', 'saturn', 'uranus',
        'neptune', 'pluto']
    :param str input_ts:  Filename with data in 'ISOdate,value'
        format or '-' for stdin.
    :param str start_date:  The start_date of the series in
        ISOdatetime format, or 'None' for beginning.
    :param str end_date:  The end_date of the series in
        ISOdatetime format, or 'None' for end.
    :param freq:  To use this form --start_date and --end_date must be
        supplied also.  The pandas date offset code used to create the
        index.
    """
    if input_ts is not None:
        start_date = input_ts.index[0]
        end_date = input_ts.index[-1]
    tindex = pd.date_range(start=start_date, end=end_date, freq=freq)
    usets = pd.DataFrame([0.0] * len(tindex), index=tindex)
    # Finish!!!!!


@cltoolbox.command(formatter_class=RSTHelpFormatter)
def risesettransit(
    latitude, longitude, start_date, end_date, body, h0=0, times="rise,set"
):
    """Print out rise, set, and/or transit times.

    :param latitude <float>:  Earth observer latitude in decimal degrees
    :param longitude <float>:  Earth observer longitude in decimal degrees
    :param start_date <str>:  ISO 8601 date string
    :param end_date <str>:  ISO 8601 date string
    :param body <str>:  Astronomical body, one of::

            Sun
            Moon
            Mercury
            Venus
            Mars
            Jupiter
            Saturn
            Uranus
            Neptune
            Pluto
    :param h0 <float>:  Earth observer standard altitude in radians
    :param times <str>: Comma separated list of times to include::

            "rise" for the rise time
            "set" for the set time
            "transit" for the transit time

        Defaults to "rise,set".
    """
    start_date = tsutils.parsedate(start_date)
    end_date = tsutils.parsedate(end_date)

    dr = pd.date_range(start=start_date, end=end_date).to_julian_date()
    start_jd = cal_to_jd(start_date)

    #
    # We need nutation values for each of three days
    #
    nutation = {}
    for day in (-1, 0, 1):
        jd = start_jd + day
        # nutation in longitude
        deltaPsi = nutation_in_longitude(jd)
        # apparent obliquity
        eps = obliquity(jd) + nutation_in_obliquity(jd)
        nutation[day] = deltaPsi, eps

    for day in (-1, 0, 1):
        jd = start_jd + day
        deltaPsi, eps = nutation[day]
        if body == "Moon":
            l, b, r = moon.dimension3(jd)
            # nutation in longitude
            l += deltaPsi
            # equatorial coordinates
            ra, dec = ecl_to_equ(l, b, eps)
        elif body == "Sun":
            l, b, r = sun.dimension3(jd)
            # correct vsop coordinates
            l, b = vsop_to_fk5(jd, l, b)
            # nutation in longitude
            l += deltaPsi
            # aberration
            l += aberration_low(r)
            # equatorial coordinates
            ra, dec = ecl_to_equ(l, b, eps)
        else:
            ra, dec = geocentric_planet(jd, body, deltaPsi, eps, days_per_second)


def main():
    if not os.path.exists("debug_astronomia"):
        sys.tracebacklimit = 0
    cltoolbox.main()


if __name__ == "__main__":
    main()
