'''
Tests for the elp2000 functions.
'''

from unittest import TestCase

from astronomia.util import interpolate3, equ_to_ecl, ecl_to_equ, d_to_r, r_to_d

class TestUtil(TestCase):
    def test_interpolate3(self):
        y = interpolate3(0.18125, (0.884226, 0.877366, 0.870531))

        self.assertAlmostEqual(y, 0.876125, places=6)


