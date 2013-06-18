'''
Tests for the elp2000 functions.
'''

from unittest import TestCase

from astronomia import elp2000
from astronomia.util import r_to_d

_elp = elp2000.ELP2000()

_comp_longitude = 133.162655*3600*1000
_comp_latitude = -3.229126
_comp_radius = 368409.7

class TestELP(TestCase):
    def test_dimension3(self):
        calc_longitude, calc_latitude, calc_radius = \
                _elp.dimension3(2448724.5)
        calc_longitude = r_to_d(calc_longitude)*3600*1000
        calc_latitude = r_to_d(calc_latitude)

        self.assertAlmostEqual(calc_longitude, _comp_longitude, delta=5)
        self.assertAlmostEqual(calc_longitude - _comp_longitude, -4.05, places=0)
        self.assertAlmostEqual(calc_latitude, _comp_latitude, places=5)
        self.assertAlmostEqual(calc_radius, _comp_radius, places=1)

    def test_dimension(self):
        calc_longitude = _elp.dimension(2448724.5, 'L')
        calc_longitude = r_to_d(calc_longitude)*3600*1000
        calc_latitude = _elp.dimension(2448724.5, 'B')
        calc_latitude = r_to_d(calc_latitude)
        calc_radius = _elp.dimension(2448724.5, 'R')

        self.assertAlmostEqual(calc_longitude, _comp_longitude, delta=5)
        self.assertAlmostEqual(calc_longitude - _comp_longitude, -4.05, places=0)
        self.assertAlmostEqual(calc_latitude, _comp_latitude, places=5)
        self.assertAlmostEqual(calc_radius, _comp_radius, places=1)

