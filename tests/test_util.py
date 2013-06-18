'''
Tests for the elp2000 functions.
'''

from unittest import TestCase

from astronomia.util import interpolate3, equ_to_ecl, ecl_to_equ, d_to_r, r_to_d

class TestUtil(TestCase):
    def test_interpolate3(self):
        y = interpolate3(0.18125, (0.884226, 0.877366, 0.870531))

        self.assertAlmostEqual(y, 0.876125, places=6)

    def test_equ_to_ecl(self):
        longitude, latitude = equ_to_ecl(d_to_r(116.328942), d_to_r(28.026183), d_to_r(23.4392911))

        self.assertAlmostEqual(r_to_d(longitude), 113.215630, places=6)
        self.assertAlmostEqual(r_to_d(latitude), 6.684170, places=6)

    def test_ecl_to_equ(self):
        ra, dec = ecl_to_equ(d_to_r(113.215630), d_to_r(6.684170), d_to_r(23.4392911))
        self.assertAlmostEqual(r_to_d(ra), 116.328942, places=5)
        self.assertAlmostEqual(r_to_d(dec), 28.026183, places=6)


