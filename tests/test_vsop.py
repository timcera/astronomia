'''
Tests for the elp2000 functions.
'''

from unittest import TestCase

from astronomia.constants import km_per_au, days_per_second, pi2
from astronomia.util import r_to_d, dms_to_d, d_to_r
from astronomia.vsop87d import VSOP87d, geocentric_planet
from astronomia.calendar import hms_to_fday

vsop = VSOP87d()

class TestVSOP(TestCase):
    def test_dimension3(self):
        L, B, R = vsop.dimension3(2448976.5, 'Venus')
        self.assertAlmostEqual(r_to_d(L) * 3600, 26.11428 * 3600, delta=0.58)
        self.assertAlmostEqual(r_to_d(B) * 3600, -2.62070 * 3600, delta=0.35)
        self.assertAlmostEqual(R * km_per_au, 0.724603 * km_per_au, delta=199)

    def test_geocentric_planet(self):
        ra, dec = geocentric_planet(2448976.5, "Venus", d_to_r(dms_to_d(0, 0, 16.749)), d_to_r(23.439669), days_per_second)
        self.assertAlmostEqual(r_to_d(ra), r_to_d(hms_to_fday(21, 4, 41.454) * pi2), places=5)
        self.assertAlmostEqual(r_to_d(dec), dms_to_d(-18, 53, 16.84), places=5)


