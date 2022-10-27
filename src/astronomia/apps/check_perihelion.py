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

A throw-away script. How fast does the radius vector change
around the time of summer solstice?

Usage:

    ./check_perihelion.py

"""

from astronomia.calendar import cal_to_jd
from astronomia.constants import km_per_au
from astronomia.planets import VSOP87d
from astronomia.util import load_params


def main():
    load_params()
    vsop = VSOP87d()

    exact_jd = cal_to_jd(1991, 7, 6 + (15.46 / 24))

    exact_r = vsop.dimension(exact_jd, "Earth", "R")

    days_per_hour = 1.0 / 24

    for i in range(-24, 24):
        jd = exact_jd + i * days_per_hour
        R = vsop.dimension(jd, "Earth", "R")
        print(i, (exact_r - R) * km_per_au)


if __name__ == "__main__":
    main()
