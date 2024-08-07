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

Geocentric solar position and radius, both low and high precision.
"""

import numpy as np

from . import calendar
from . import globals as globls
from .calendar import jd_to_jcent
from .coordinates import ecl_to_equ
from .nutation import nutation_in_longitude, obliquity
from .planets import VSOP87d, vsop_to_fk5
from .util import _scalar_if_one, d_to_r, dms_to_d, modpi2, polynomial


class Error(Exception):
    """Local exception class."""


class Sun:
    """High precision position calculations.

    This is a very light wrapper around the VSOP87d class. The
    geocentric longitude of the Sun is simply the heliocentric longitude
    of the Earth + 180 degrees. The geocentric latitude of the Sun is
    the negative of the heliocentric latitude of the Earth. The radius
    is of course the same in both coordinate systems.
    """

    def __init__(self):
        self.vsop = VSOP87d()

    def mean_longitude(self, jd):
        """Return mean longitude.

        Arguments:
          - `jd` : Julian Day in dynamical time

        Returns:
          - Longitude in radians
        """
        jd = np.atleast_1d(jd)
        T = jd_to_jcent(jd)

        # From astrolabe
        # X = polynomial((d_to_r(100.466457),
        #                d_to_r(36000.7698278),
        #                d_to_r(0.00030322),
        #                d_to_r(0.000000020)), T)

        # From AA, Naughter
        # Takes T/10.0
        X = polynomial(
            (
                d_to_r(100.4664567),
                d_to_r(360007.6982779),
                d_to_r(0.03032028),
                d_to_r(1.0 / 49931),
                d_to_r(-1.0 / 15300),
                d_to_r(-1.0 / 2000000),
            ),
            T / 10.0,
        )

        X = modpi2(X + np.pi)
        return _scalar_if_one(X)

    def mean_longitude_perigee(self, jd):
        """Return mean longitude of solar perigee.

        Arguments:
          - `jd` : Julian Day in dynamical time

        Returns:
          - Longitude of solar perigee in radians
        """
        jd = np.atleast_1d(jd)
        T = jd_to_jcent(jd)

        X = polynomial((1012395.0, 6189.03, 1.63, 0.012), (T + 1)) / 3600.0
        X = d_to_r(X)

        X = modpi2(X)
        return _scalar_if_one(X)

    def dimension(self, jd, dim):
        """Return one of geocentric ecliptic longitude, latitude and radius.

        Arguments:
          - jd : Julian Day in dynamical time
          - dim : one of "L" (longitude) or "B" (latitude) or "R" (radius).

        Returns:
          - Either longitude in radians, or latitude in radians, or radius in
            au, depending on value of `dim`.
        """
        jd = np.atleast_1d(jd)
        X = self.vsop.dimension(jd, "Earth", dim)
        if dim == "L":
            X = modpi2(X + np.pi)
        elif dim == "B":
            X = -X
        return _scalar_if_one(X)

    def dimension3(self, jd):
        """Return geocentric ecliptic longitude, latitude and radius.

        Arguments:
          - `jd` : Julian Day in dynamical time

        Returns:
          - longitude in radians
          - latitude in radians
          - radius in au
        """
        L = self.dimension(jd, "L")
        B = self.dimension(jd, "B")
        R = self.dimension(jd, "R")
        return L, B, R


#
# Constant terms
#
_kL0 = (d_to_r(280.46646), d_to_r(36000.76983), d_to_r(0.0003032))
_kM = (
    d_to_r(357.5291092),
    d_to_r(35999.0502909),
    d_to_r(-0.0001536),
    d_to_r(1.0 / 24490000),
)
_kC = (d_to_r(1.914602), d_to_r(-0.004817), d_to_r(-0.000014))

_ck3 = d_to_r(0.019993)
_ck4 = d_to_r(-0.000101)
_ck5 = d_to_r(0.000289)


def longitude_radius_low(jd):
    """Return geometric longitude and radius vector.

    Low precision. The longitude is accurate to 0.01 degree.  The latitude
    should be presumed to be 0.0. [Meeus-1998: equations 25.2 through 25.5

    Arguments:
      - `jd` : Julian Day in dynamical time

    Returns:
      - longitude in radians
      - radius in au
    """
    jd = np.atleast_1d(jd)
    T = jd_to_jcent(jd)
    L0 = polynomial(_kL0, T)
    M = polynomial(_kM, T)
    er = polynomial((0.016708634, -0.000042037, -0.0000001267), T)
    C = (
        polynomial(_kC, T) * np.sin(M)
        + (_ck3 - _ck4 * T) * np.sin(2 * M)
        + _ck5 * np.sin(3 * M)
    )
    L = modpi2(L0 + C)
    v = M + C
    R = 1.000001018 * (1 - er * er) / (1 + er * np.cos(v))
    return L, R


#
# Constant terms
#
_lk0 = d_to_r(125.04)
_lk1 = d_to_r(1934.136)
_lk2 = d_to_r(0.00569)
_lk3 = d_to_r(0.00478)


def apparent_longitude_low(jd, L):
    """Correct the geometric longitude for nutation and aberration.

    Low precision. [Meeus-1998: pg 164]

    Arguments:
      - `jd` : Julian Day in dynamical time
      - `L` : longitude in radians

    Returns:
      - corrected longitude in radians
    """
    jd = np.atleast_1d(jd)
    T = jd_to_jcent(jd)
    omega = _lk0 - _lk1 * T
    return _scalar_if_one(modpi2(L - _lk2 - _lk3 * np.sin(omega)))


#
# Constant terms
#
_lk4 = d_to_r(dms_to_d(0, 0, 20.4898))


def aberration_low(R):
    """Correct for aberration; low precision, but good enough for most uses.

    [Meeus-1998: pg 164]

    Arguments:
      - `R` : radius in au

    Returns:
      - correction in radians
    """
    return -_lk4 / R


def rise(
    year,
    month,
    day,
    longitude=globls.longitude,
    latitude=globls.latitude,
    gregorian=True,
):
    from .constants import sun_rst_altitude

    jd = calendar.cal_to_jd(year, month, day, gregorian=gregorian)

    sun = Sun()
    #
    # Sun
    #
    sun_longitude, sun_latitude, sun_radius = sun.dimension3(jd)

    # correct vsop coordinates
    sun_longitude, sun_latitude = vsop_to_fk5(jd, sun_longitude, sun_latitude)

    # nutation in longitude
    sun_longitude += nutation_in_longitude(jd)

    # aberration
    sun_longitude += aberration_low(sun_radius)

    # equatorial coordinates
    ra, dec = ecl_to_equ(sun_longitude, sun_latitude, obliquity(jd))

    obj = sun
    del obj.raList[0]
    del obj.decList[0]
    del obj.h0List[0]
    obj.raList.append(ra)
    obj.decList.append(dec)
    obj.h0List.append(sun_rst_altitude)
