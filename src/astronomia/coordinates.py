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

Collection of miscellaneous functions
"""

import numpy as np

from astronomia import globals as globls
from astronomia.util import modpi2


class Error(Exception):
    """Local exception class."""


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
    cose = np.cos(obliquity)
    sine = np.sin(obliquity)
    sinl = np.sin(longitude)
    ra = modpi2(np.arctan2(sinl * cose - np.tan(latitude) * sine, np.cos(longitude)))
    dec = np.arcsin(np.sin(latitude) * cose + np.cos(latitude) * sine * sinl)
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
    cosH = np.cos(H)
    sinLat = np.sin(globls.latitude)
    cosLat = np.cos(globls.latitude)
    A = np.arctan2(np.sin(H), cosH * sinLat - np.tan(decl) * cosLat)
    h = np.arcsin(sinLat * np.sin(decl) + cosLat * np.cos(decl) * cosH)
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
    from .constants import earth_equ_radius

    f = 1.0 / 298.2564219846
    ea = earth_equ_radius / 1000

    ee = 2.0 * f - f * f

    sinLat = np.sin(latitude)
    cosLat = np.cos(latitude)

    N = ea / np.sqrt(1.0 - ee * sinLat * sinLat)

    Hx = (N + height) * cosLat
    Hy = (N * (1 - ee) + height) * sinLat

    r = np.sqrt(Hx * Hx + Hy * Hy)
    theta = np.arctan2(Hx, Hy)
    phi = longitude

    return (r, theta, phi)


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
    cose = np.cos(obliquity)
    sine = np.sin(obliquity)
    sina = np.sin(ra)
    longitude = modpi2(np.arctan2(sina * cose + np.tan(dec) * sine, np.cos(ra)))
    latitude = modpi2(np.arcsin(np.sin(dec) * cose - np.cos(dec) * sine * sina))
    return longitude, latitude
