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

The VSOP87d planetary position model
"""

import numpy as np

from .calendar import jd_to_jcent
from .constants import pi2
from .coordinates import ecl_to_equ
from .util import _scalar_if_one, d_to_r, diff_angle, dms_to_d, modpi2, polynomial


class Error(Exception):
    """Local exception class."""

    pass


#
# Global values, readable from other modules
#
planet_names = (
    "Mercury",
    "Venus",
    "Earth",
    "Mars",
    "Jupiter",
    "Saturn",
    "Uranus",
    "Neptune",
)
coordinate_names = ("L", "B", "R")

#
# Local dictionary of planetary terms.
#
# The key is a tuple (planet_name, coordinate_name)
#
# The value of each entry is a list of lists.
#
_planets = {}

_first_time = True


class VSOP87d:
    """The VSOP87d planetary model.

    All instances of this class share a common dictionary of planetary
    terms.
    """

    def __init__(self):
        """Load the database of planetary terms.

        This is actually done only once to save time and space.
        """
        global _first_time

        if not _first_time:
            return

        global _planets
        from .vsop87d_dict import _planets

        _first_time = False

    def dimension(self, jd, planet, dim):
        """Return one of heliocentric ecliptic longitude, latitude and radius.

        [Meeus-1998: pg 218]

        Arguments:
          - `jd`     : Julian Day in dynamical time
          - `planet` : must be one of ("Mercury", "Venus", "Earth", "Mars",
            "Jupiter", "Saturn", "Uranus", "Neptune")
          - `dim`    : must be one of "L" (longitude) or "B" (latitude) or "R"
            (radius)

        Returns:
          - longitude in radians, or latitude in radians, or radius in au,
            depending on the value of `dim`.
        """
        jd = np.atleast_1d(jd)
        X = 0.0
        tauN = 1.0
        tau = jd_to_jcent(jd) / 10.0
        c = _planets[(planet, dim)]

        for s in c:
            X += np.sum([A * np.cos(B + C * tau) for A, B, C in s]) * tauN
            tauN = tauN * tau  # last calculation is wasted

        if dim == "L":
            X = modpi2(X)

        return _scalar_if_one(X)

    def dimension3(self, jd, planet):
        """Return heliocentric ecliptic longitude, latitude and radius.

        Arguments:
          - `jd`     : Julian Day in dynamical time
          - `planet` : must be one of ("Mercury", "Venus", "Earth", "Mars",
            "Jupiter", "Saturn", "Uranus", "Neptune")

        Returns:
          - longitude in radians
          - latitude in radians
          - radius in au
        """
        L = self.dimension(jd, planet, "L")
        B = self.dimension(jd, planet, "B")
        R = self.dimension(jd, planet, "R")
        return L, B, R


#
# Constant terms
#
_k0 = d_to_r(-1.397)
_k1 = d_to_r(-0.00031)
_k2 = d_to_r(dms_to_d(0, 0, -0.09033))
_k3 = d_to_r(dms_to_d(0, 0, 0.03916))


def vsop_to_fk5(jd, L, B):
    """Convert VSOP to FK5 coordinates.

    This is required only when using the full precision of the
    VSOP model.  [Meeus-1998: pg 219]

    Arguments:
      - `jd` : Julian Day in dynamical time
      - `L`  : longitude in radians
      - `B`  : latitude in radians

    Returns:
      - corrected longitude in radians
      - corrected latitude in radians
    """
    jd = np.atleast_1d(jd)
    T = jd_to_jcent(jd)
    L1 = polynomial([L, _k0, _k1], T)
    cosL1 = np.cos(L1)
    sinL1 = np.sin(L1)
    deltaL = _k2 + _k3 * (cosL1 + sinL1) * np.tan(B)
    deltaB = _k3 * (cosL1 - sinL1)
    return _scalar_if_one(modpi2(L + deltaL)), _scalar_if_one(B + deltaB)


def geocentric_planet(jd, planet, deltaPsi, epsilon, delta):
    """Calculate the equatorial coordinates of a planet.

    The results will be geocentric, corrected for light-time and
    aberration.

    Arguments:
      - `jd`       : Julian Day in dynamical time
      - `planet`   : must be one of ("Mercury", "Venus", "Earth", "Mars",
        "Jupiter", "Saturn", "Uranus", "Neptune")
      - `deltaPsi` : nutation in longitude, in radians
      - `epsilon`  : True obliquity (corrected for nutation), in radians
      - `delta`    : desired accuracy, in days

    Returns:
      - right accension, in radians
      - declination, in radians
    """
    jd = np.atleast_1d(jd)
    vsop = VSOP87d()
    t = jd
    l0 = -100.0  # impossible value
    # We need to iterate to correct for light-time and aberration.
    # At most three passes through the loop always nails it.
    # Note that we move both the Earth and the other planet during
    #    the iteration.
    for bailout in range(20):
        # heliocentric geometric ecliptic coordinates of the Earth
        L0, B0, R0 = vsop.dimension3(t, "Earth")

        # heliocentric geometric ecliptic coordinates of the planet
        L, B, R = vsop.dimension3(t, planet)

        # rectangular offset
        cosB0 = np.cos(B0)
        cosB = np.cos(B)
        x = R * cosB * np.cos(L) - R0 * cosB0 * np.cos(L0)
        y = R * cosB * np.sin(L) - R0 * cosB0 * np.sin(L0)
        z = R * np.sin(B) - R0 * np.sin(B0)

        # geocentric geometric ecliptic coordinates of the planet
        x2 = x * x
        y2 = y * y
        l = np.arctan2(y, x)
        b = np.arctan2(z, np.sqrt(x2 + y2))

        # distance to planet in AU
        dist = np.sqrt(x2 + y2 + z * z)

        # light time in days
        tau = 0.0057755183 * dist

        if abs(diff_angle(l, l0)) < pi2 * delta:
            break

        # adjust for light travel time and try again
        l0 = l
        t = jd - tau
    else:
        raise Error("bailout")

    # transform to FK5 ecliptic and equinox
    l, b = vsop_to_fk5(jd, l, b)

    # nutation in longitude
    l = l + deltaPsi

    # equatorial coordinates
    ra, dec = ecl_to_equ(l, b, epsilon)

    return ra, dec
