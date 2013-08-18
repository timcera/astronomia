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

    Collection of miscellaneous functions
    """

from math import modf, cos, sin, asin, tan, atan2, pi
import os
import shlex
import sys

import numpy as np

import astronomia.globals
from astronomia.constants import pi2, minutes_per_day, seconds_per_day
from astronomia.util import _scalar_if_one, modpi2


class Error(Exception):
    """Local exception class"""
    pass


def ecl_to_equ(longitude, latitude, obliquity):
    """Convert ecliptic to equitorial coordinates.

    [Meeus-1998: equations 13.3, 13.4]

    Arguments:
      - `longitude` : ecliptic longitude in radians
      - `latitude` : ecliptic latitude in radians
      - `obliquity` : obliquity of the ecliptic in radians

    Returns:
      - Right accension in radians
      - Declination in radians

    """
    cose = cos(obliquity)
    sine = sin(obliquity)
    sinl = sin(longitude)
    ra = modpi2(atan2(sinl * cose - tan(latitude) * sine, cos(longitude)))
    dec = asin(sin(latitude) * cose + cos(latitude) * sine * sinl)
    return ra, dec


def equ_to_horiz(H, decl):
    """Convert equitorial to horizontal coordinates.

    [Meeus-1998: equations 13.5, 13.6]

    Note that azimuth is measured westward starting from the south.

    This is not a good formula for using near the poles.

    Arguments:
      - `H` : hour angle in radians
      - `decl` : declination in radians

    Returns:
      - azimuth in radians
      - altitude in radians

    """
    cosH = cos(H)
    sinLat = sin(astronomia.globals.latitude)
    cosLat = cos(astronomia.globals.latitude)
    A = atan2(sin(H), cosH * sinLat - tan(decl) * cosLat)
    h = asin(sinLat * sin(decl) + cosLat * cos(decl) * cosH)
    return A, h


def ell_to_geo(latitude, longitude, height):
    """Convert elliptic to geocentric coordinates.

    Arguments:
      - `latitude` : latitude
      - `longitude` : longitude
      - `height` : height

    Returns:
      - r
      - theta
      - phi

    """
    from constants import earth_equ_radius

    f = 1.0/298.2564219846
    ea = earth_equ_radius/1000

    ee = 2.0*f - f*f

    sinLat = sin(astronomia.globals.latitude)
    cosLat = cos(astronomia.globals.latitude)

    N = ea/np.sqrt(1.0 - ee*sin_lat*sin_lat)

    Hx = (N + height)*cos_lat
    Hy = (N*(1 - ee) + height)*sin_lat

    r = np.sqrt(Hx*Hx + Hy*Hy)
    theta = np.aran2(Hx, Hy)
    phi = longitude

    return(r, theta, ph)


def equ_to_ecl(ra, dec, obliquity):
    """Convert equitorial to ecliptic coordinates.

    [Meeus-1998: equations 13.1, 13.2]

    Arguments:
      - `ra` : right accension in radians
      - `dec` : declination in radians
      - `obliquity` : obliquity of the ecliptic in radians

    Returns:
      - ecliptic longitude in radians
      - ecliptic latitude in radians

    """
    cose = cos(obliquity)
    sine = sin(obliquity)
    sina = sin(ra)
    longitude = modpi2(atan2(sina * cose + tan(dec) * sine, cos(ra)))
    latitude = modpi2(asin(sin(dec) * cose - cos(dec) * sine * sina))
    return longitude, latitude

