#! /usr/bin/env python
"""
    Astrolabe copyright 2000, 2001 William McClain
    Astrolabe forked to Astronomia 2013
    Astronomia copyright 2013

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

from heapq import heappop, heappush
from math import *

import cltoolbox
from cltoolbox.rst_text_formatter import RSTHelpFormatter

import astronomia.globals
from astronomia.calendar import cal_to_jd, easter, lt_to_str, ut_to_lt
from astronomia.constants import (
    days_per_minute,
    days_per_second,
    standard_rst_altitude,
    sun_rst_altitude,
)
from astronomia.coordinates import ecl_to_equ
from astronomia.dynamical import dt_to_ut
from astronomia.equinox import equinox, equinox_approx
from astronomia.lunar import Lunar
from astronomia.nutation import nutation_in_longitude, nutation_in_obliquity, obliquity
from astronomia.planets import VSOP87d, geocentric_planet, planet_names, vsop_to_fk5
from astronomia.riseset import moon_rst_altitude, rise, settime, transit
from astronomia.sun import Sun, aberration_low
from astronomia.util import load_params

vsop = None  # delay loading this until we are sure the script can run
sun = None  # "                  "
moon = Lunar()

HIGH_PRIORITY = 0.0

rstDict = {}


class Task:
    def __init__(self, jd, func, args):
        self.jd = jd
        self.func = func
        self.args = args

    def __cmp__(self, other):
        return cmp(self.jd, other.jd)

    def __gt__(self, other):
        return self.jd > other.jd


taskQueue = []


class RiseSetTransit:
    def __init__(self, name, raList, decList, h0List):
        self.name = name
        self.raList = raList
        self.decList = decList
        self.h0List = h0List


def display(str):
    print(str)


def doEaster(year):
    month, day = easter(year)
    jd = cal_to_jd(year, month, day)
    str = f"{lt_to_str(jd, None, 'day'):<24} Easter"
    heappush(taskQueue, Task(jd, display, (str,)))
    # recalculate on March 1, next year
    heappush(taskQueue, Task(cal_to_jd(year + 1, 3, 1), doEaster, (year + 1,)))


_seasons = {
    "spring": "Vernal Equinox",
    "summer": "Summer Solstice",
    "autumn": "Autumnal Equinox",
    "winter": "Winter Solstice",
}


def doEquinox(year, season):
    approx_jd = equinox_approx(year, season)
    jd = equinox(approx_jd, season, days_per_second)
    ut = dt_to_ut(jd)
    lt, zone = ut_to_lt(ut)
    str = f"{lt_to_str(lt, zone)} {_seasons[season]}"
    heappush(taskQueue, Task(jd, display, (str,)))
    heappush(taskQueue, Task(jd, doEquinox, (year + 1, season)))


def doRiseSetTransit(jd_today):
    #
    # Find and queue rise-set-transit times for all objects
    #
    jd = jd_today
    for obj in list(rstDict.values()):
        if td := rise(jd, obj.raList, obj.decList, obj.h0List[1], days_per_minute):
            ut = dt_to_ut(td)
            lt, zone = ut_to_lt(ut)
            str = f"{lt_to_str(lt, '', 'minute'):<19} {zone} {obj.name} rises"
            heappush(taskQueue, Task(td, display, (str,)))
        else:
            print("****** RiseSetTransit failure:", obj.name, "rise")

        if td := settime(jd, obj.raList, obj.decList, obj.h0List[1], days_per_minute):
            ut = dt_to_ut(td)
            lt, zone = ut_to_lt(ut)
            str = f"{lt_to_str(lt, '', 'minute'):<19} {zone} {obj.name} sets"
            heappush(taskQueue, Task(td, display, (str,)))
        else:
            print("****** RiseSetTransit failure:", obj.name, "set")

        if td := transit(jd, obj.raList, days_per_second):
            ut = dt_to_ut(td)
            lt, zone = ut_to_lt(ut)
            str = f"{lt_to_str(lt, zone):<23} {obj.name} transits"
            heappush(taskQueue, Task(td, display, (str,)))
        else:
            print("****** RiseSetTransit failure:", obj.name, "transit")

    #
    # setup the day after tomorrow
    #
    jd += 2

    # nutation in longitude
    deltaPsi = nutation_in_longitude(jd)

    # apparent obliquity
    eps = obliquity(jd) + nutation_in_obliquity(jd)

    #
    # Planets
    #
    for planet in planet_names:
        if planet == "Earth":
            continue
        ra, dec = geocentric_planet(jd, planet, deltaPsi, eps, days_per_second)
        obj = rstDict[planet]
        del obj.raList[0]
        del obj.decList[0]
        del obj.h0List[0]
        obj.raList.append(ra)
        obj.decList.append(dec)
        obj.h0List.append(standard_rst_altitude)
    #
    # Moon
    #
    l, b, r = moon.dimension3(jd)

    # nutation in longitude
    l += deltaPsi

    # equatorial coordinates
    ra, dec = ecl_to_equ(l, b, eps)

    obj = rstDict["Moon"]
    del obj.raList[0]
    del obj.decList[0]
    del obj.h0List[0]
    obj.raList.append(ra)
    obj.decList.append(dec)
    obj.h0List.append(moon_rst_altitude(r))

    #
    # Sun
    #
    l, b, r = sun.dimension3(jd)

    # correct vsop coordinates
    l, b = vsop_to_fk5(jd, l, b)

    # nutation in longitude
    l += deltaPsi

    # aberration
    l += aberration_low(r)

    # equatorial coordinates
    ra, dec = ecl_to_equ(l, b, eps)

    obj = rstDict["Sun"]
    del obj.raList[0]
    del obj.decList[0]
    del obj.h0List[0]
    obj.raList.append(ra)
    obj.decList.append(dec)
    obj.h0List.append(sun_rst_altitude)

    heappush(taskQueue, Task(jd, doRiseSetTransit, (jd_today + 1,)))


def initRST(start_year):
    start_jd = cal_to_jd(start_year)

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

    #
    # Planets
    #
    for planet in planet_names:
        if planet == "Earth":
            continue
        raList = []
        decList = []
        h0List = []
        for day in (-1, 0, 1):
            jd = start_jd + day
            deltaPsi, eps = nutation[day]
            ra, dec = geocentric_planet(jd, planet, deltaPsi, eps, days_per_second)
            raList.append(ra)
            decList.append(dec)
            h0List.append(standard_rst_altitude)
        rstDict[planet] = RiseSetTransit(planet, raList, decList, h0List)

    #
    # Moon
    #
    raList = []
    decList = []
    h0List = []
    for day in (-1, 0, 1):
        jd = start_jd + day
        deltaPsi, eps = nutation[day]
        l, b, r = moon.dimension3(jd)
        # nutation in longitude
        l += deltaPsi
        # equatorial coordinates
        ra, dec = ecl_to_equ(l, b, eps)
        raList.append(ra)
        decList.append(dec)
        h0List.append(moon_rst_altitude(r))
    rstDict["Moon"] = RiseSetTransit("Moon", raList, decList, h0List)

    #
    # Sun
    #
    raList = []
    decList = []
    h0List = []
    for day in (-1, 0, 1):
        jd = start_jd + day
        deltaPsi, eps = nutation[day]
        l, b, r = sun.dimension3(jd)
        # correct vsop coordinates
        l, b = vsop_to_fk5(jd, l, b)
        # nutation in longitude
        l += deltaPsi
        # aberration
        l += aberration_low(r)
        # equatorial coordinates
        ra, dec = ecl_to_equ(l, b, eps)
        raList.append(ra)
        decList.append(dec)
        h0List.append(sun_rst_altitude)
    rstDict["Sun"] = RiseSetTransit("Sun", raList, decList, h0List)

    # all Rise-Set-Transit events
    heappush(taskQueue, Task(HIGH_PRIORITY, doRiseSetTransit, (start_jd,)))


@cltoolbox.command(formatter_class=RSTHelpFormatter)
def cronus(start, stop=None):
    """Displays a variety of celestial events in the order they occur.

    To do::

        -- Add many more events
        -- Support both real-time and "fast" modes
        -- Allow finer start and stop times

    Currently the program always runs in "fast" mode, queueing and
    displaying events in the future as fast as possible. Eventually
    I would like to have enough events covered so that the display
    runs continuously even in real-time. Since the next event of
    a given type needs to be calculated only when the previous one
    has been delivered, this is not as computationally intense as it
    sounds.

    Parameters
    ----------
    start : int
        The year to start the display.
    stop : int, optional
        The year to stop the display. If not given, the display
        continues until 10,000AD.
    """
    global vsop
    global sun
    start = int(start)
    stop = cal_to_jd(stop) if stop is None else int(stop)
    load_params()
    vsop = VSOP87d()
    sun = Sun()

    # Easter
    heappush(taskQueue, Task(HIGH_PRIORITY, doEaster, (start,)))

    # four equinox/solstice events
    for season in astronomia.globals.season_names:
        heappush(taskQueue, Task(HIGH_PRIORITY, doEquinox, (start, season)))

    # initialize rise-set-transit objects
    initRST(start)

    # start the task loop
    t = heappop(taskQueue)
    while t.jd < stop:
        t.func(*t.args)
        t = heappop(taskQueue)


def main():
    cltoolbox.main()


if __name__ == "__main__":
    main()
