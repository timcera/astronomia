"""
Tests for the elp2000 functions.
"""

from unittest import TestCase

from astronomia.util import interpolate3, interpolate_angle3


class TestUtil(TestCase):
    def test_interpolate3(self):
        y = interpolate3(0.18125, (0.884226, 0.877366, 0.870531))

        self.assertAlmostEqual(y, 0.876125, places=6)

    def test_interpolate_angle3(self):
        y = interpolate_angle3(0, (359, 0, 1))

        self.assertAlmostEqual(y, 0.0, places=6)
