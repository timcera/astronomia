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

from typing import Tuple, Union

import numpy as np

from astronomia import globals as globls
from astronomia.util import modpi2

ArrayLike = Union[float, np.ndarray, list]


class Error(Exception):
    """Local exception class."""


def ecl_to_equ(
    longitude: ArrayLike, latitude: ArrayLike, obliquity: ArrayLike
) -> Tuple[ArrayLike, ArrayLike]:
    """
    Convert ecliptic to equatorial coordinates.

    [Meeus-1998: equations 13.3, 13.4]

    Parameters
    ----------
    longitude
        Ecliptic longitude in radians.
    latitude
        Ecliptic latitude in radians.
    obliquity
        Obliquity of the ecliptic in radians.

    Returns
    -------
    right_ascension
        Right ascension in radians
    declination
        Declination in radians
    """
    cose = np.cos(obliquity)
    sine = np.sin(obliquity)
    sinl = np.sin(longitude)
    ra = modpi2(np.arctan2(sinl * cose - np.tan(latitude) * sine, np.cos(longitude)))
    dec = np.arcsin(np.sin(latitude) * cose + np.cos(latitude) * sine * sinl)
    return ra, dec


def equ_to_horiz(H: ArrayLike, decl: ArrayLike) -> Tuple[ArrayLike, ArrayLike]:
    """
    Convert equatorial to horizontal coordinates.

    [Meeus-1998: equations 13.5, 13.6]

    Parameters
    ----------
    H
        Hour angle in radians.
    decl
        Declination in radians.

    Returns
    -------
    azimuth
        azimuth in radians
    altitude
        altitude in radians

    Notes
    -----
    Azimuth is measured westward starting from the south. This formula is not
    accurate near the poles.
    """
    cosH = np.cos(H)
    sinLat = np.sin(globls.latitude)
    cosLat = np.cos(globls.latitude)
    A = np.arctan2(np.sin(H), cosH * sinLat - np.tan(decl) * cosLat)
    h = np.arcsin(sinLat * np.sin(decl) + cosLat * np.cos(decl) * cosH)
    return A, h


def ell_to_geo(
    latitude: ArrayLike, longitude: ArrayLike, height: ArrayLike
) -> Tuple[ArrayLike, ArrayLike, ArrayLike]:
    """
    Convert elliptic to geocentric coordinates.

    Parameters
    ----------
    latitude
        Latitude in radians.
    longitude
        Longitude in radians.
    height
        Height above the ellipsoid in kilometers.

    Returns
    -------
    r
        Distance from the center of the Earth in kilometers.
    theta
        Angle from the x-axis in radians.
    phi
        Angle from the z-axis in radians.
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


def equ_to_ecl(
    ra: ArrayLike, dec: ArrayLike, obliquity: ArrayLike
) -> Tuple[ArrayLike, ArrayLike]:
    """
    Convert equatorial to ecliptic coordinates.

    [Meeus-1998: equations 13.1, 13.2]

    Parameters
    ----------
    ra
        Right ascension in radians.
    dec
        Declination in radians.
    obliquity
        Obliquity of the ecliptic in radians.

    Returns
    -------
    ecliptic_longitude
        Ecliptic longitude in radians
    ecliptic_latitude
        Ecliptic latitude in radians.
    """
    cose = np.cos(obliquity)
    sine = np.sin(obliquity)
    sina = np.sin(ra)
    longitude = modpi2(np.arctan2(sina * cose + np.tan(dec) * sine, np.cos(ra)))
    latitude = modpi2(np.arcsin(np.sin(dec) * cose - np.cos(dec) * sine * sina))
    return longitude, latitude
