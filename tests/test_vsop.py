"""
Tests for the elp2000 functions.
"""

from unittest import TestCase
import os.path

import numpy as np

from astronomia.constants import km_per_au, days_per_second, pi2
from astronomia.util import r_to_d, dms_to_d, d_to_r
from astronomia.planets import VSOP87d, geocentric_planet
from astronomia.calendar import hms_to_fday

vsop = VSOP87d()


class TestVSOP(TestCase):
    def test_dimension3(self):
        L, B, R = vsop.dimension3(2448976.5, "Venus")
        np.testing.assert_array_almost_equal(
            r_to_d(L) * 3600, 26.11428 * 3600, decimal=0
        )
        np.testing.assert_array_almost_equal(
            r_to_d(B) * 3600, -2.62070 * 3600, decimal=0
        )
        np.testing.assert_array_almost_equal(
            R * km_per_au, 0.724603 * km_per_au, decimal=-4
        )

    def test_geocentric_planet(self):
        ra, dec = geocentric_planet(
            2448976.5,
            "Venus",
            d_to_r(dms_to_d(0, 0, 16.749)),
            d_to_r(23.439669),
            days_per_second,
        )
        np.testing.assert_array_almost_equal(
            r_to_d(ra), r_to_d(hms_to_fday(21, 4, 41.454) * pi2), decimal=5
        )
        np.testing.assert_almost_equal(r_to_d(dec), dms_to_d(-18, 53, 16.84), decimal=5)


class TestVSOPDatabase(TestCase):
    def test_vsop87d_chk(self):
        """
        where "vsop87.chk" has been fetched from the ftp directory referenced
        at:

            http://cdsweb.u-strasbg.fr/cgi-bin/Cat?VI/81

        The program scans through the file and selects those 80 tests which
        apply to VSOP87d. We calculate results for each test and compare
        with the given value.

        Result: all calculations match within 1e-10 radians or au.

        """
        refs = []
        bname = os.path.dirname(__file__)
        f = open(os.path.join(bname, "vsop87.chk"), "r")
        line = f.readline()
        while line:
            fields = line.split()
            if fields:
                if fields[0] == "VSOP87D":
                    planet = fields[1]
                    planet = planet[0] + planet[1:].lower()
                    jd = fields[2]
                    jd = float(jd[2:])
                    line = f.readline()
                    fields = line.split()
                    l = float(fields[1])
                    b = float(fields[4])
                    r = float(fields[7])
                    refs.append((planet, jd, l, b, r))
            line = f.readline()
        f.close()

        for planet, jd, l, b, r in refs:
            L, B, R = vsop.dimension3(jd, planet)
            np.testing.assert_array_almost_equal(L, l)
            np.testing.assert_array_almost_equal(B, b)
            np.testing.assert_array_almost_equal(R, r)
