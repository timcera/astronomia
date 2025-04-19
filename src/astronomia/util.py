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

import os
import shlex

import numpy as np

from . import globals as globls
from .constants import minutes_per_day, pi2, seconds_per_day


class Error(Exception):
    """Local exception class."""


def _scalar_if_one(solution):
    """
    Return a scalar if the array size is 1.

    Parameters
    ----------
    solution : ndarray or scalar
        Input value or array.

    Returns
    -------
    scalar or ndarray
        Scalar if the input array size is 1, otherwise the input value.
    """
    if np.isscalar(solution):
        return solution
    return solution.item() if solution.size == 1 else solution


def d_to_dms(x):
    """
    Convert an angle in decimal degrees to degree components.

    Parameters
    ----------
    x : float
        Angle in decimal degrees.

    Returns
    -------
    degrees : int
        Degrees component.
    minutes : int
        Minutes component.
    seconds : float
        Seconds component.
    """
    frac, degrees = np.modf(x)
    seconds, minutes = np.modf(frac * 60)
    return int(degrees), int(minutes), seconds * 60


def d_to_r(d):
    """
    Convert degrees to radians.

    Parameters
    ----------
    d : float
        Angle in degrees.

    Returns
    -------
    d_to_r
        Angle in radians.
    """
    return d * np.pi / 180.0


def r_to_d(r):
    """
    Convert radians to degrees.

    Parameters
    ----------
    r : float
        Angle in radians.

    Returns
    -------
    r_to_d
        Angle in degrees.
    """
    return r * 180.0 / np.pi


def diff_angle(a, b):
    """
    Return the difference between two angles, accounting for circular values.

    Parameters
    ----------
    a : float
        First angle in radians.
    b : float
        Second angle in radians.

    Returns
    -------
    diff_angle
        Difference between the two angles in radians, in the range -pi to pi.
    """
    result = b + pi2 - a if b < a else b - a
    if result > np.pi:
        result -= pi2
    return result


def dms_to_d(deg, minute, sec):
    """
    Convert an angle in degree components to decimal degrees.

    Parameters
    ----------
    deg : float
        Degrees component.
    minute : float
        Minutes component.
    sec : float
        Seconds component.

    Returns
    -------
    dms_to_d
        Angle in decimal degrees.
    """
    deg = np.atleast_1d(deg)
    minute = np.atleast_1d(minute)
    sec = np.atleast_1d(sec)
    deg, minute, sec = np.broadcast_arrays(deg, minute, sec)
    result = abs(deg) + abs(minute) / 60.0 + abs(sec) / 3600.0
    if deg < 0 or minute < 0 or sec < 0:
        result = -result
    return _scalar_if_one(result)


def interpolate3(n, y):
    """
    Interpolate from three equally spaced tabular values.

    [Meeus-1998; equation 3.3]

    Parameters
    ----------
    n : float
        Interpolating factor, must be between -1 and 1.
    y : sequence of float
        Sequence of three values.

    Returns
    -------
    interpolate3
        Interpolated value.
    """
    if not -1 < n < 1:
        raise Error(f"interpolating factor out of range: {n}")

    a = y[1] - y[0]
    b = y[2] - y[1]
    c = b - a
    return y[1] + n / 2 * (a + b + n * c)


def interpolate_angle3(n, y):
    """
    Interpolate from three equally spaced tabular angular values.

    [Meeus-1998; equation 3.3]

    Parameters
    ----------
    n : float
        Interpolating factor, must be between -1 and 1.
    y : sequence of float
        Sequence of three angular values.

    Returns
    -------
    interpolate_angle3
        Interpolated angular value.
    """
    if not -1 < n < 1:
        raise Error(f"interpolating factor out of range: {n}")

    a = diff_angle(y[0], y[1])
    b = diff_angle(y[1], y[2])
    c = diff_angle(a, b)
    return y[1] + n / 2 * (a + b + n * c)


def load_params():
    """
    Read a parameter file and assign global values.

    Parameters
    ----------
    None

    Returns
    -------
    None
    """
    fname = os.environ.get("ASTRONOMIA_PARAMS", "astronomia_params.txt")

    if not os.path.exists(fname):
        # last resort
        fname = os.path.join(
            os.path.dirname(__file__),
            os.path.pardir,
            "share",
            "astronomia",
            "astronomia_params.txt",
        )
        print(
            f"""WARNING: Using system wide settings file at
"{fname}".
You may want to set the ASTRONOMIA_PARAMS environment variable to point to the
file you want, or create a "astronomia_params.txt" file in the current
directory."""
        )
    if not os.path.exists(fname):
        # really last resort
        fname = os.path.join(
            os.path.dirname(__file__),
            os.path.pardir,
            os.path.pardir,
            "params",
            "astronomia_params.txt",
        )
        print(
            f"""WARNING: Using system wide settings file at
"{fname}".
You may want to set the ASTRONOMIA_PARAMS environment variable to point to the
file you want, or create a "astronomia_params.txt" file in the current
directory."""
        )
    if not os.path.exists(fname):
        # really last resort
        fname = os.path.join(
            os.path.dirname(__file__),
            "astronomia_params.txt",
        )
        print(
            f"""WARNING: Using system wide settings file at
"{fname}".
You may want to set the ASTRONOMIA_PARAMS environment variable to point to the
file you want, or create a "astronomia_params.txt" file in the current
directory."""
        )

    try:
        f = open(fname)
    except OSError as value:
        raise Error(
            """
Unable to open param file. Either set ASTRONOMIA_PARAMS correctly or create
astronomia_params.txt in the current directory"""
        ) from value

    lex = shlex.shlex(f)
    # tokens and values can have dots, dashes, slashes, colons
    lex.wordchars = f"{lex.wordchars}.-/\\:"
    while token := lex.get_token():
        if token == "standard_timezone_name":
            globls.standard_timezone_name = lex.get_token()
        elif token == "standard_timezone_offset":
            offset = float(lex.get_token())
            unit = lex.get_token().lower()
            if unit not in (
                "day",
                "days",
                "hour",
                "hours",
                "minute",
                "minutes",
                "second",
                "seconds",
            ):
                raise Error("bad value for standard_timezone_offset units")
            if unit in ("hour", "hours"):
                offset /= 24.0
            elif unit in ("minute", "minutes"):
                offset /= minutes_per_day
            elif unit in ("second", "seconds"):
                offset /= seconds_per_day
            globls.standard_timezone_offset = offset
        elif token == "daylight_timezone_name":
            globls.daylight_timezone_name = lex.get_token()
        elif token == "daylight_timezone_offset":
            offset = float(lex.get_token())
            unit = lex.get_token().lower()
            if unit not in (
                "day",
                "days",
                "hour",
                "hours",
                "minute",
                "minutes",
                "second",
                "seconds",
            ):
                raise Error("bad value for standard_timezone_offset units")
            if unit in ("hour", "hours"):
                offset /= 24.0
            elif unit in ("minute", "minutes"):
                offset /= minutes_per_day
            elif unit in ("second", "seconds"):
                offset /= seconds_per_day
            globls.daylight_timezone_offset = offset
        elif token == "longitude":
            longitude = float(lex.get_token())
            direction = lex.get_token().lower()
            if direction not in ("east", "west"):
                raise Error('longitude direction must be "west" or "east"')
            if direction == "east":
                longitude = -longitude
            globls.longitude = d_to_r(longitude)
        elif token == "latitude":
            latitude = float(lex.get_token())
            direction = lex.get_token().lower()
            if direction not in ("north", "south"):
                raise Error('latitude direction must be "north" or "south"')
            if direction == "south":
                latitude = -latitude
            globls.latitude = d_to_r(latitude)
        elif token == "vsop87d_text_path":
            globls.vsop87d_text_path = lex.get_token()
        elif token == "vsop87d_binary_path":
            globls.vsop87d_binary_path = lex.get_token()
        else:
            raise Error("unknown token {token} at line {lex.lineno} in param file")
    f.close()


def modpi2(x):
    """
    Reduce an angle in radians to the range 0..2pi.

    Parameters
    ----------
    x : float
        Angle in radians.

    Returns
    -------
    modpi2
        Angle in radians in the range 0..2pi.
    """
    return x % pi2


def mod360(x):
    """
    Reduce an angle in degrees to the range 0..360.

    Parameters
    ----------
    x : float
        Angle in degrees.

    Returns
    -------
    mod360
        Angle in degrees in the range 0..360.
    """
    return x % 360


def polynomial(terms, x):
    """
    Evaluate a simple polynomial.

    Parameters
    ----------
    terms : sequence of float
        Coefficients of the polynomial. `terms[0]` is the constant term,
        `terms[1]` is the coefficient for x, `terms[2]` is for x^2, etc.
    x : float
        Variable value.

    Returns
    -------
    polynomial
        Value of the polynomial.

    Examples
    --------
    >>> t = 4.1
    >>> polynomial((1.1, -3.2, 3.3, 4.5), t)
    353.59749999999997
    """
    apolyfunc = np.polynomial.Polynomial(terms)
    return apolyfunc(x)
