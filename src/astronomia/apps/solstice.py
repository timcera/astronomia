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

import cltoolbox
from cltoolbox.rst_text_formatter import RSTHelpFormatter

import astronomia.globals
from astronomia.calendar import lt_to_str, ut_to_lt
from astronomia.constants import days_per_second
from astronomia.dynamical import dt_to_ut
from astronomia.equinox import equinox, equinox_approx
from astronomia.util import load_params

tab = 4 * " "


@cltoolbox.command(formatter_class=RSTHelpFormatter)
def solstice(start, stop=None):
    """Displays the instants of equinoxes and solstices for a range of years.

    Times are accurate to one second.

    Parameters
    ----------
    start : int
        The start year, or if stop is not given, the year to display.
    stop : int
        The end year.
    """
    start = int(start)
    stop = start if stop is None else int(stop)
    load_params()

    for yr in range(start, stop + 1):
        print(yr)
        for season in astronomia.globals.season_names:
            approx_jd = equinox_approx(yr, season)
            jd = equinox(approx_jd, season, days_per_second)
            ut = dt_to_ut(jd)
            lt, zone = ut_to_lt(ut)
            print(tab, season, lt_to_str(lt, zone))


def main():
    cltoolbox.main()


if __name__ == "__main__":
    main()
