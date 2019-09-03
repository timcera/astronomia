import os
import sys

import pandas as pd

import mando
from mando.rst_text_formatter import RSTHelpFormatter

from tstoolbox import tsutils
from tstoolbox.tstoolbox import createts


@mando.command(formatter_class=RSTHelpFormatter)
def right_ascension(
    latitude, longitude, body, input_ts=None, start_date=None, end_date=None, freq=None
):
    """Print out right ascension.

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
    usets = createts(
        input_ts=input_ts, start_date=start_date, end_date=end_date, freq=freq
    )
    pass


@mando.command(formatter_class=RSTHelpFormatter)
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

    raList = []
    decList = []
    h0List = []
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
            ra, dec = geocentric_planet(jd, planet, deltaPsi, eps, days_per_second)


def main():
    if not os.path.exists("debug_astronomia"):
        sys.tracebacklimit = 0
    mando.main()


if __name__ == "__main__":
    main()
