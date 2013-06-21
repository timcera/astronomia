'''
Tests for the elp2000 functions.
'''

from unittest import TestCase
import datetime

import numpy as np

from astronomia.constants import km_per_au
from astronomia.sun import longitude_radius_low, apparent_longitude_low, aberration_low, Sun
from astronomia.util import r_to_d, dms_to_d
from astronomia.vsop87d import vsop_to_fk5, VSOP87d
from astronomia.calendar import cal_to_jd, hms_to_fday

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

    def test_compare_to_schureman(self):
        rad2deg = 180.0/np.pi
        dt = [datetime.datetime(i, 1, 1) for i in range(1800,2001,20)]
        dt = dt + [datetime.datetime(1990,3,3,18,0,0)]
        dt = dt + [datetime.datetime(1999,1,10,3,0,0)]
        jd = [cal_to_jd(i.year, i.month, i.day) +
              hms_to_fday(i.hour, i.minute, i.second) for i in dt]
        jd = np.array(jd)
        h = np.mod(sun.mean_longitude(jd)*rad2deg, 360)
        p1 = np.mod(sun.mean_longitude_perigee(jd)*rad2deg, 360)

        h_schureman = [280.41,
                       279.57,
                       279.73,
                       279.88,
                       280.04,
                       280.19,
                       279.36,
                       279.51,
                       279.67,
                       279.82,
                       279.97,
                       280.39 + 58.15 + 1.97 + 0.74,
                       280.21  + 0.00  + 8.87 + 0.12]
        p1_schureman = [279.50,
                       279.85,
                       280.19,
                       280.53,
                       280.88,
                       281.22,
                       281.56,
                       281.91,
                       282.25,
                       282.60,
                       282.94,
                       282.77 +  0.00 +  0.00 + 0.00,
                       282.92  + 0.00  + 0.00 + 0.00]
        for i in range(len(h)):
            self.assertAlmostEqual(h[i], h_schureman[i], places=1)
            self.assertAlmostEqual(p1[i], p1_schureman[i], places=1)
