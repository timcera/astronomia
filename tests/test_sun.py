'''
Tests for the elp2000 functions.
'''

from unittest import TestCase

from astronomia.constants import km_per_au
from astronomia.sun import longitude_radius_low, apparent_longitude_low, aberration_low, Sun
from astronomia.util import r_to_d, dms_to_d
from astronomia.vsop87d import vsop_to_fk5, VSOP87d

sun = Sun()
vsop = VSOP87d()

class TestSun(TestCase):
    def test_longitude_radius_low(self):
        longitude, radius = longitude_radius_low(2448908.5)
        self.assertAlmostEquals(r_to_d(longitude), 199.90988, places=5)
        self.assertAlmostEquals(radius, 0.99766, places=5)

        longitude = apparent_longitude_low(2448908.5, longitude)
        self.assertAlmostEquals(r_to_d(longitude), 199.90895, places=5)

    def test_dimension3(self):
        L, B, R = sun.dimension3(2448908.5)
        self.assertAlmostEqual(r_to_d(L) * 3600, 199.907372 * 3600, places=0)
        self.assertAlmostEqual(r_to_d(B) * 3600, 0.644, delta=0.1)
        self.assertAlmostEqual(R * km_per_au, 0.99760775 * km_per_au, delta=116)
        L, B = vsop_to_fk5(2448908.5, L, B)
        self.assertAlmostEqual(r_to_d(L) * 3600, 199.907347 * 3600, delta=0.27)
        self.assertAlmostEqual(r_to_d(B) * 3600, 0.62, delta=0.11)
        aberration = aberration_low(R)
        self.assertAlmostEqual(r_to_d(aberration) * 3600, -20.539, places=3)

        self.assertAlmostEqual(r_to_d(L) * 3600 * 100, dms_to_d(199, 54, 26.18) * 3600 * 100, delta=0.1)
        self.assertAlmostEqual(r_to_d(B) * 3600 * 100, 0.72 * 100, delta=0.06)
        self.assertAlmostEqual(R, 0.99760853)


