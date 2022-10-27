from unittest import TestCase

from astronomia.coordinates import ecl_to_equ, ell_to_geo, equ_to_ecl
from astronomia.util import d_to_r, modpi2, r_to_d


class TestCoords(TestCase):
    def test_equ_to_ecl(self):
        longitude, latitude = equ_to_ecl(
            d_to_r(116.328942), d_to_r(28.026183), d_to_r(23.4392911)
        )

        self.assertAlmostEqual(r_to_d(longitude), 113.215630, places=6)
        self.assertAlmostEqual(r_to_d(latitude), 6.684170, places=6)

    def test_ecl_to_equ(self):
        ra, dec = ecl_to_equ(d_to_r(113.215630), d_to_r(6.684170), d_to_r(23.4392911))
        self.assertAlmostEqual(r_to_d(ra), 116.328942, places=5)
        self.assertAlmostEqual(r_to_d(dec), 28.026183, places=6)

    def test_ell_to_geo(self):
        phi, theta, r = ell_to_geo(d_to_r(0), d_to_r(0), 10000)
        self.assertAlmostEqual(r_to_d(modpi2(phi)), 203.23542197)
        self.assertAlmostEqual(r_to_d(modpi2(theta)), 90.0)
        self.assertAlmostEqual(r, 0.0)
