'''
Tests for the elp2000 functions.
'''

from unittest import TestCase

from astronomia.nutation import nut_in_lon, nut_in_obl, obliquity, obliquity_hi
from astronomia.util import d_to_dms, r_to_d

class TestNutaiont(TestCase):
    def test_nut_in_lon(self):
        deltaPsi = nut_in_lon(2446895.5)
        d, m, s = d_to_dms(r_to_d(deltaPsi))
        self.assertEqual(d, 0)
        self.assertEqual(m, 0)
        self.assertAlmostEqual(s, -3.788, places=3)

    def test_nut_in_obl(self):
        deltaEps = nut_in_obl(2446895.5)
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

