'''
Tests for the elp2000 functions.
'''

from unittest import TestCase

from astronomia.util import interpolate3

class TestUtil(TestCase):
    def test_interpolate3(self):
        y = interpolate3(0.18125, (0.884226, 0.877366, 0.870531))

        self.assertAlmostEqual(y, 0.876125, places=6)


