"""
Tests for the elp2000 functions.
"""

from unittest import TestCase

from astronomia.nutation import (
    nutation_in_longitude,
    nutation_in_obliquity,
    obliquity,
    obliquity_hi,
)
from astronomia.util import d_to_dms, r_to_d


class TestNutation(TestCase):
    def test_nut_in_lon(self):
        deltaPsi = nutation_in_longitude(2446895.5)
        d, m, s = d_to_dms(r_to_d(deltaPsi))
        self.assertEqual(d, 0)
        self.assertEqual(m, 0)
        self.assertAlmostEqual(s, -3.788, places=3)

        # from http://www.neoprogrammics.com/nutations/Nutation_In_Longitude_And_RA.php
        deltaPsi = nutation_in_longitude(2456479.5)
        d, m, s = d_to_dms(r_to_d(deltaPsi))
        self.assertEqual(d, 0)
        self.assertEqual(m, 0)
        self.assertAlmostEqual(s, 12.675, places=3)

    def test_nut_in_obl(self):
        deltaEps = nutation_in_obliquity(2446895.5)
        d, m, s = d_to_dms(r_to_d(deltaEps))
        self.assertEqual(d, 0)
        self.assertEqual(m, 0)
        self.assertAlmostEqual(s, 9.443, places=3)

    def test_obliquity(self):
        eps = obliquity(2446895.5)
        d, m, s = d_to_dms(r_to_d(eps))
        self.assertEqual(d, 23)
        self.assertEqual(m, 26)
        self.assertAlmostEqual(s, 27.407, places=3)

    def test_obliquity_hi(self):
        eps = obliquity_hi(2446895.5)
        d, m, s = d_to_dms(r_to_d(eps))
        self.assertEqual(d, 23)
        self.assertEqual(m, 26)
        self.assertAlmostEqual(s, 27.407, places=3)
