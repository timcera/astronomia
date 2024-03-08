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

Lunar position model ELP2000-82 of Chapront.

The result values are for the equinox of date and have been adjusted
for light-time.

This is the simplified version of Jean Meeus, *Astronomical Algorithms*,
second edition, 1998, Willmann-Bell, Inc.
"""

import numpy as np

from .calendar import jd_to_jcent
from .commonterms import kD, kF, kL1, kM, kM1, ko
from .util import d_to_r, modpi2, polynomial


class Error(Exception):
    """Local exception class."""

    pass


# [Meeus-1998: table 47.A]
#
#    D, M, M1, F, l, r


_tblLR = (
    (0, 0, 1, 0, 6288774, -20905355),
    (2, 0, -1, 0, 1274027, -3699111),
    (2, 0, 0, 0, 658314, -2955968),
    (0, 0, 2, 0, 213618, -569925),
    (0, 1, 0, 0, -185116, 48888),
    (0, 0, 0, 2, -114332, -3149),
    (2, 0, -2, 0, 58793, 246158),
    (2, -1, -1, 0, 57066, -152138),
    (2, 0, 1, 0, 53322, -170733),
    (2, -1, 0, 0, 45758, -204586),
    (0, 1, -1, 0, -40923, -129620),
    (1, 0, 0, 0, -34720, 108743),
    (0, 1, 1, 0, -30383, 104755),
    (2, 0, 0, -2, 15327, 10321),
    (0, 0, 1, 2, -12528, 0),
    (0, 0, 1, -2, 10980, 79661),
    (4, 0, -1, 0, 10675, -34782),
    (0, 0, 3, 0, 10034, -23210),
    (4, 0, -2, 0, 8548, -21636),
    (2, 1, -1, 0, -7888, 24208),
    (2, 1, 0, 0, -6766, 30824),
    (1, 0, -1, 0, -5163, -8379),
    (1, 1, 0, 0, 4987, -16675),
    (2, -1, 1, 0, 4036, -12831),
    (2, 0, 2, 0, 3994, -10445),
    (4, 0, 0, 0, 3861, -11650),
    (2, 0, -3, 0, 3665, 14403),
    (0, 1, -2, 0, -2689, -7003),
    (2, 0, -1, 2, -2602, 0),
    (2, -1, -2, 0, 2390, 10056),
    (1, 0, 1, 0, -2348, 6322),
    (2, -2, 0, 0, 2236, -9884),
    (0, 1, 2, 0, -2120, 5751),
    (0, 2, 0, 0, -2069, 0),
    (2, -2, -1, 0, 2048, -4950),
    (2, 0, 1, -2, -1773, 4130),
    (2, 0, 0, 2, -1595, 0),
    (4, -1, -1, 0, 1215, -3958),
    (0, 0, 2, 2, -1110, 0),
    (3, 0, -1, 0, -892, 3258),
    (2, 1, 1, 0, -810, 2616),
    (4, -1, -2, 0, 759, -1897),
    (0, 2, -1, 0, -713, -2117),
    (2, 2, -1, 0, -700, 2354),
    (2, 1, -2, 0, 691, 0),
    (2, -1, 0, -2, 596, 0),
    (4, 0, 1, 0, 549, -1423),
    (0, 0, 4, 0, 537, -1117),
    (4, -1, 0, 0, 520, -1571),
    (1, 0, -2, 0, -487, -1739),
    (2, 1, 0, -2, -399, 0),
    (0, 0, 2, -2, -381, -4421),
    (1, 1, 1, 0, 351, 0),
    (3, 0, -2, 0, -340, 0),
    (4, 0, -3, 0, 330, 0),
    (2, -1, 2, 0, 327, 0),
    (0, 2, 1, 0, -323, 1165),
    (1, 1, -1, 0, 299, 0),
    (2, 0, 3, 0, 294, 0),
    (2, 0, -1, -2, 0, 8752),
)

# [Meeus-1998: table 47.B]
#
#    D, M, M1, F, b

_tblB = (
    (0, 0, 0, 1, 5128122),
    (0, 0, 1, 1, 280602),
    (0, 0, 1, -1, 277693),
    (2, 0, 0, -1, 173237),
    (2, 0, -1, 1, 55413),
    (2, 0, -1, -1, 46271),
    (2, 0, 0, 1, 32573),
    (0, 0, 2, 1, 17198),
    (2, 0, 1, -1, 9266),
    (0, 0, 2, -1, 8822),
    (2, -1, 0, -1, 8216),
    (2, 0, -2, -1, 4324),
    (2, 0, 1, 1, 4200),
    (2, 1, 0, -1, -3359),
    (2, -1, -1, 1, 2463),
    (2, -1, 0, 1, 2211),
    (2, -1, -1, -1, 2065),
    (0, 1, -1, -1, -1870),
    (4, 0, -1, -1, 1828),
    (0, 1, 0, 1, -1794),
    (0, 0, 0, 3, -1749),
    (0, 1, -1, 1, -1565),
    (1, 0, 0, 1, -1491),
    (0, 1, 1, 1, -1475),
    (0, 1, 1, -1, -1410),
    (0, 1, 0, -1, -1344),
    (1, 0, 0, -1, -1335),
    (0, 0, 3, 1, 1107),
    (4, 0, 0, -1, 1021),
    (4, 0, -1, 1, 833),
    (0, 0, 1, -3, 777),
    (4, 0, -2, 1, 671),
    (2, 0, 0, -3, 607),
    (2, 0, 2, -1, 596),
    (2, -1, 1, -1, 491),
    (2, 0, -2, 1, -451),
    (0, 0, 3, -1, 439),
    (2, 0, 2, 1, 422),
    (2, 0, -3, -1, 421),
    (2, 1, -1, 1, -366),
    (2, 1, 0, 1, -351),
    (4, 0, 0, 1, 331),
    (2, -1, 1, 1, 315),
    (2, -2, 0, -1, 302),
    (0, 0, 1, 3, -283),
    (2, 1, 1, -1, -229),
    (1, 1, 0, -1, 223),
    (1, 1, 0, 1, 223),
    (0, 1, -2, -1, -220),
    (2, 1, -1, -1, -220),
    (1, 0, 1, 1, -185),
    (2, -1, -2, -1, 181),
    (0, 1, 2, 1, -177),
    (4, 0, -2, -1, 176),
    (4, -1, -1, -1, 166),
    (1, 0, 1, -1, -164),
    (4, 0, 1, -1, 132),
    (1, 0, -1, -1, -119),
    (4, -1, 0, -1, 115),
    (2, -2, 0, 1, 107),
)

_kA1 = (d_to_r(119.75), d_to_r(131.849))
_kA2 = (d_to_r(53.09), d_to_r(479264.290))
_kA3 = (d_to_r(313.45), d_to_r(481266.484))


def _constants(T):
    """Calculate values required by several other functions."""
    L1 = modpi2(polynomial(kL1, T))
    D = modpi2(polynomial(kD, T))
    M = modpi2(polynomial(kM, T))
    M1 = modpi2(polynomial(kM1, T))
    F = modpi2(polynomial(kF, T))

    A1 = modpi2(polynomial(_kA1, T))
    A2 = modpi2(polynomial(_kA2, T))
    A3 = modpi2(polynomial(_kA3, T))

    E = polynomial([1.0, -0.002516, -0.0000074], T)
    E2 = E * E

    return L1, D, M, M1, F, A1, A2, A3, E, E2


class Lunar:
    """ELP2000 lunar position calculations."""

    def mean_longitude_ascending_node(self, jd):
        """Return mean longitude of ascending node.

        Current implemention in astronomia is from:

           PJ Naughter (Web: www.naughter.com, Email: pjna@naughter.com)

        Previous implementation.

        Another equation from:
           This routine is part of the International Astronomical Union's
           SOFA (Standards of Fundamental Astronomy) software collection.
           Fundamental (Delaunay) arguments from Simon et al. (1994)

        *  Arcseconds to radians
           DOUBLE PRECISION DAS2R
           PARAMETER ( DAS2R = 4.848136811095359935899141D-6 )

        *  Milliarcseconds to radians
           DOUBLE PRECISION DMAS2R
           PARAMETER ( DMAS2R = DAS2R / 1D3 )

        *  Arc seconds in a full circle
           DOUBLE PRECISION TURNAS
           PARAMETER ( TURNAS = 1296000D0 )

        *  Mean longitude of the ascending node of the Moon.
           OM  = MOD ( 450160.398036D0  -6962890.5431D0*T, TURNAS ) * DAS2R

        Arguments:
          - `jd` : julian Day

        Returns:
          - mean longitude of ascending node
        """
        T = jd_to_jcent(jd)
        return modpi2(polynomial(ko, T))

    def mean_longitude_perigee(self, jd):
        """Return mean longitude of lunar perigee.

        Arguments:
          - `jd` : julian Day

        Returns:
          - mean longitude of perigee
        """
        T = jd_to_jcent(jd)
        X = polynomial(
            (
                d_to_r(83.3532465),
                d_to_r(4069.0137287),
                d_to_r(-0.0103200),
                d_to_r(-1.0 / 80053),
                d_to_r(1.0 / 18999000),
            ),
            T,
        )
        return modpi2(X)

    def mean_longitude(self, jd):
        """Return geocentric mean longitude.

        Arguments:
          - `jd` : Julian Day in dynamical time

        Returns:
          - mean longitude in radians
        """
        T = jd_to_jcent(jd)
        return modpi2(polynomial(kL1, T))

    def mean_elongation(self, jd):
        """Return geocentric mean elongation.

        Arguments:
          - `jd` : Julian Day in dynamical time

        Returns:
          - mean elongation in radians
        """
        T = jd_to_jcent(jd)
        return modpi2(polynomial(kD, T))

    def mean_anomaly(self, jd):
        """Return geocentric mean anomaly.

        Arguments:
          - `jd` : Julian Day in dynamical time

        Returns:
          - mean anomaly in radians
        """
        T = jd_to_jcent(jd)
        return modpi2(polynomial(kM1, T))

    def argument_of_latitude(self, jd):
        """Return geocentric mean longitude.

        Arguments:
          - `jd` : Julian Day in dynamical time

        Returns:
          - argument of latitude in radians
        """
        T = jd_to_jcent(jd)
        return modpi2(polynomial(kF, T))

    def dimension3(self, jd):
        """Return geocentric ecliptic longitude, latitude and radius.

        When we need all three dimensions it is more efficient to combine the
        calculations in one routine.

        Arguments:
          - `jd` : Julian Day in dynamical time

        Returns:
          - longitude in radians
          - latitude in radians
          - radius in km, Earth's center to Moon's center
        """
        return self._longitude(jd), self._latitude(jd), self._radius(jd)

    def dimension(self, jd, dim):
        """Return one of geocentric ecliptic longitude, latitude and radius.

        Arguments:
          - `jd` : Julian Day in dynamical time
          - `dim` : "L" (longitude") or "B" (latitude) or "R" (radius)

        Returns:
          - longitude in radians or latitude in radians or radius in km,
            Earth's center to Moon's center, depending on value of `dim`.
        """
        if dim == "L":
            return self._longitude(jd)
        if dim == "B":
            return self._latitude(jd)
        if dim == "R":
            return self._radius(jd)
        raise Error(f"unknown dimension = {dim}")

    def _longitude(self, jd):
        """Return the geocentric ecliptic longitude in radians."""
        from .nutation import nutation_in_longitude

        T = jd_to_jcent(jd)
        L1, D, M, M1, F, A1, A2, A3, E, E2 = _constants(T)
        lsum = 0.0
        for tD, tM, tM1, tF, tl, tr in _tblLR:
            arg = tD * D + tM * M + tM1 * M1 + tF * F
            if abs(tM) == 1:
                tl *= E
            elif abs(tM) == 2:
                tl *= E2
            lsum += tl * np.sin(arg)

        lsum += 3958 * np.sin(A1) + 1962 * np.sin(L1 - F) + 318 * np.sin(A2)

        nutinlong = nutation_in_longitude(jd)
        return L1 + d_to_r(lsum / 1000000) + nutinlong

    def _latitude(self, jd):
        """Return the geocentric ecliptic latitude in radians."""
        T = jd_to_jcent(jd)
        L1, D, M, M1, F, A1, A2, A3, E, E2 = _constants(T)

        bsum = 0.0
        for tD, tM, tM1, tF, tb in _tblB:
            arg = tD * D + tM * M + tM1 * M1 + tF * F
            if abs(tM) == 1:
                tb *= E
            elif abs(tM) == 2:
                tb *= E2
            bsum += tb * np.sin(arg)

        bsum += (
            -2235 * np.sin(L1)
            + 382 * np.sin(A3)
            + 175 * np.sin(A1 - F)
            + 175 * np.sin(A1 + F)
            + 127 * np.sin(L1 - M1)
            - 115 * np.sin(L1 + M1)
        )

        return d_to_r(bsum / 1000000)

    def _radius(self, jd):
        """Return the geocentric radius in km."""
        T = jd_to_jcent(jd)
        L1, D, M, M1, F, A1, A2, A3, E, E2 = _constants(T)

        rsum = 0.0
        for tD, tM, tM1, tF, tl, tr in _tblLR:
            arg = tD * D + tM * M + tM1 * M1 + tF * F
            if abs(tM) == 1:
                tr *= E
            elif abs(tM) == 2:
                tr *= E2
            rsum += tr * np.cos(arg)

        return 385000.56 + rsum / 1000
