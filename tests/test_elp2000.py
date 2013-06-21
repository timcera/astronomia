'''
Tests for the elp2000 functions.
'''

from unittest import TestCase
import datetime

import numpy as np

from astronomia import elp2000
from astronomia.util import r_to_d
from astronomia.calendar import cal_to_jd, hms_to_fday

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

    def test_compare_to_schureman(self):
        rad2deg = 180.0/np.pi
        dt = [datetime.datetime(i, 1, 1) for i in range(1800,2001,20)]
        dt = dt + [datetime.datetime(1990,3,3,18,0,0)]
        dt = dt + [datetime.datetime(1999,1,10,3,0,0)]
        jd = [cal_to_jd(i.year, i.month, i.day) +
              hms_to_fday(i.hour, i.minute, i.second) for i in dt]
        jd = np.array(jd)
        Nv = np.mod(_elp.mean_longitude_ascending_node(jd)*rad2deg, 360)
        p = np.mod(_elp.mean_longitude_perigee(jd)*rad2deg, 360)
        s = np.mod(_elp.mean_longitude(jd)*rad2deg, 360)

        Nv_schureman = [33.25,
                         6.47,
                       339.64,
                       312.81,
                       285.98,
                       259.16,
                       232.38,
                       205.55,
                       178.72,
                       151.89,
                       125.07,
                       318.45 - 3.12 - 0.11 - 0.04,
                       144.39 + 0.00 - 0.48 - 0.01]
        p_schureman = [225.45,
                       319.15,
                        52.96,
                       146.77,
                       240.58,
                       334.38,
                        68.08,
                       161.88,
                       255.69,
                       349.49,
                        83.29,
                        36.45 + 6.57 + 0.22 + 0.08,
                        42.63 + 0.00 + 1.00 + 0.01]
        s_schureman = [342.31,
                       102.71,
                       236.29,
                         9.87,
                       143.45,
                       277.03,
                        37.43,
                       171.01,
                       304.59,
                        78.16,
                       211.74,
                       np.mod(331.54 + 57.41 + 26.35 + 9.88, 360),
                       82.36  + 0.00  + 118.59 + 1.65]
        for i in range(len(Nv)):
            self.assertAlmostEqual(Nv[i], Nv_schureman[i], places=1)
            self.assertAlmostEqual(p[i], p_schureman[i], places=1)
            self.assertAlmostEqual(s[i], s_schureman[i], places=1)

